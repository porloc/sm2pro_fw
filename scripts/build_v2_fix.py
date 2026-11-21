#!/usr/bin/env python3
"""
Исправление ошибки [0007] "Внутренняя ошибка микропрограммы адаптера (FLASH/MCU)".

Причина: в собранном ранее образе 2.22.3 EEPROM-слоты 3-8 (адреса 0x08002886-0x08002891),
в которые штатное обновление записывает {crc, ver, size} приложения, остались пустыми
(0xFF от донорского дампа 2.21.32). Загрузчик-стаб 2.22.3 при команде запуска 0x37
сравнивает 3 слова из этих слотов с ожидаемыми ПК значениями {ver=0x1198,
crc=0x210E9A13, size=0x1353C} и при несовпадении отвечает статусом 7, который
ПК-программа показывает как [0007].

Дополнительно обновляется загрузочная запись (boot record) EEPROM @0x08002800:
{crc, ver, size} — её ver используется ответом команды 0x83 (INFO) бутлоадера;
ПК-программа сравнивает его с ожидаемой версией прошивки.

EEPROM slot -> адрес: 0x08002800 + (slot + 0x40)*2  (сервисы 5/6 бутлоадера)
  slot3 @0x08002886, slot4 @0x08002888  -> size (мл./ст. половины)
  slot5 @0x0800288A, slot6 @0x0800288C  -> ver
  slot7 @0x0800288E, slot8 @0x08002890  -> crc
Идентификация stub'а (get_identification 0x08004604):
  word_ver  = slot6<<16 | slot5    (сравнивается с body+0 команды 0x37)
  word_crc  = slot8<<16 | slot7    (сравнивается с body+4)
  word_size = slot4<<16 | slot3    (сравнивается с body+8)
"""
import struct
import hashlib
import zlib

OUT = '/home/z/my-project/fw_analysis/OUTPUT'

# Официальные параметры приложения 2.22.3 (из sm2lib.dll 2.22.3, функция 0x1000C760)
APP_CRC = 0x210E9A13   # CRC32(STM32) официального приложения 2.22.3
APP_VER = 0x1198       # версия 2.22.3
APP_SIZE = 0x1353C     # размер приложения

def wr_half(img, addr, val):
    off = addr - 0x08000000
    img[off:off+2] = struct.pack('<H', val & 0xFFFF)

def apply_eeprom_fix(img):
    """Записать слоты 3-8 (идентификация запуска) и boot record."""
    # слоты идентификации (адрес = 0x08002800 + (slot+0x40)*2)
    wr_half(img, 0x08002886, APP_SIZE & 0xFFFF)          # slot3 = size low
    wr_half(img, 0x08002888, (APP_SIZE >> 16) & 0xFFFF)  # slot4 = size high
    wr_half(img, 0x0800288A, APP_VER & 0xFFFF)           # slot5 = ver low
    wr_half(img, 0x0800288C, (APP_VER >> 16) & 0xFFFF)   # slot6 = ver high
    wr_half(img, 0x0800288E, APP_CRC & 0xFFFF)           # slot7 = crc low
    wr_half(img, 0x08002890, (APP_CRC >> 16) & 0xFFFF)   # slot8 = crc high
    # загрузочная запись @0x08002800: {crc, ver, size} — ver отдаётся командой 0x83
    img[0x2800:0x280C] = struct.pack('<III', APP_CRC, APP_VER, APP_SIZE)
    return img

def apply_eeprom_fix_slots_only(img):
    """Только слоты 3-8, boot record (ver для 0x83) оставить донорский (0x1070)."""
    wr_half(img, 0x08002886, APP_SIZE & 0xFFFF)
    wr_half(img, 0x08002888, (APP_SIZE >> 16) & 0xFFFF)
    wr_half(img, 0x0800288A, APP_VER & 0xFFFF)
    wr_half(img, 0x0800288C, (APP_VER >> 16) & 0xFFFF)
    wr_half(img, 0x0800288E, APP_CRC & 0xFFFF)
    wr_half(img, 0x08002890, (APP_CRC >> 16) & 0xFFFF)
    return img

def md5(b): return hashlib.md5(b).hexdigest()
def sha256(b): return hashlib.sha256(b).hexdigest()

def crc32_stm32(d):
    """CRC сервиса бутлоадера (опкод 9): rbit+CRC-блок+~ — эквивалент zlib CRC-32."""
    return zlib.crc32(d) & 0xFFFFFFFF

def report(name, data):
    print(f"{name}: {len(data)} bytes")
    print(f"  MD5:    {md5(data)}")
    print(f"  SHA256: {sha256(data)}")

def main():
    results = []

    # 1) Основной исправленный образ: патч клона (9 слов UID) + EEPROM-слоты + boot record
    base = open(f'{OUT}/SM2Pro_full_flash_2.22.3_patched.bin', 'rb').read()
    img = apply_eeprom_fix(bytearray(base))
    # контроль: приложение в образе = patched (CRC 0xBB7A85CE), а слоты содержат
    # ОФИЦИАЛЬНЫЙ crc 0x210E9A13 — именно его присылает ПК в 0x37, и именно с ним
    # сравнивает stub (CRC при запуске не пересчитывается)
    assert crc32_stm32(bytes(img[0x5000:0x5000+APP_SIZE])) == 0xBB7A85CE
    open(f'{OUT}/SM2Pro_full_flash_2.22.3_patched_v2.bin', 'wb').write(bytes(img))
    results.append(('SM2Pro_full_flash_2.22.3_patched_v2.bin', bytes(img)))

    # 2) Вариант только со слотами (boot record донорский 0x1070) — запасной
    img2 = apply_eeprom_fix_slots_only(bytearray(base))
    open(f'{OUT}/SM2Pro_full_flash_2.22.3_patched_v2_slots_only.bin', 'wb').write(bytes(img2))
    results.append(('SM2Pro_full_flash_2.22.3_patched_v2_slots_only.bin', bytes(img2)))

    # 3) Официальное приложение + исправленный EEPROM (без патча клона)
    base3 = open(f'{OUT}/SM2Pro_full_flash_2.22.3_restored.bin', 'rb').read()
    img3 = apply_eeprom_fix(bytearray(base3))
    assert crc32_stm32(bytes(img3[0x5000:0x5000+APP_SIZE])) == APP_CRC
    open(f'{OUT}/SM2Pro_full_flash_2.22.3_official_v2.bin', 'wb').write(bytes(img3))
    results.append(('SM2Pro_full_flash_2.22.3_official_v2.bin', bytes(img3)))

    print("=== Готово. Хэши: ===")
    for name, data in results:
        report(name, data)

    # Верификация слотов в готовых образах
    print("\n=== Проверка EEPROM исправленного образа ===")
    v = results[0][1]
    print(f"boot record @0x2800: crc=0x{struct.unpack('<I', v[0x2800:0x2804])[0]:08X} "
          f"ver=0x{struct.unpack('<I', v[0x2804:0x2808])[0]:04X} "
          f"size=0x{struct.unpack('<I', v[0x2808:0x280C])[0]:X}")
    for slot in range(3, 9):
        addr = 0x08002800 + (slot + 0x40) * 2
        val = struct.unpack('<H', v[addr - 0x08000000:addr - 0x08000000 + 2])[0]
        print(f"slot{slot} @0x{addr:08X} = 0x{val:04X}")
    ver_w = struct.unpack('<H', v[0x288C:0x288E])[0] << 16 | struct.unpack('<H', v[0x288A:0x288C])[0]
    crc_w = struct.unpack('<H', v[0x2890:0x2892])[0] << 16 | struct.unpack('<H', v[0x288E:0x2890])[0]
    size_w = struct.unpack('<H', v[0x2888:0x288A])[0] << 16 | struct.unpack('<H', v[0x2886:0x2888])[0]
    print(f"\nИдентификация запуска (слоты): ver=0x{ver_w:08X} crc=0x{crc_w:08X} size=0x{size_w:08X}")
    print(f"Ожидает ПК:                    ver=0x{APP_VER:08X} crc=0x{APP_CRC:08X} size=0x{APP_SIZE:08X}")
    assert ver_w == APP_VER and crc_w == APP_CRC and size_w == APP_SIZE
    print("СОВПАДЕНИЕ — команда 0x37 пройдёт, приложение запустится.")

if __name__ == '__main__':
    main()
