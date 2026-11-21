#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Сборка полного дампа SM2Pro с прошивкой 2.22.3 (из Scanmatik 2.22.3) + патч клона.

Карта флеша нового формата (STM32F105VCT6, 256КБ):
  0x08000000-0x08003FFF  бутлоадер + EEPROM стр.1/2   <- донорский дамп (проверен)
                          (в EEPROM по 0x080028E8 «виртуальный UID» клона:
                           слово 0x3247F69E, байт 0x43 по 0x080028F3)
  0x08004000-0x08004AFF  stub-загрузчик 2.22.3 (0xB00)   <- sm2lib.dll 2.22.3 (CRC 0x2912D0A0)
  0x08004B00-0x08004FFF  0xFF
  0x08005000-0x0801853B  основное приложение 2.22.3 (0x1353C) <- sm2lib.dll 2.22.3 (CRC 0x210E9A13)
  0x0801853C-0x0803FFFF  0xFF

Патч (аналог найденного в донорском дампе 2.21.32):
  во всех 9 пулах литералов приложения слово 0x1FFFF7E8 (адрес 96-битного UID
  STM32 в системной памяти) заменяется на 0x080028E8 (адрес «виртуального UID»
  в EEPROM) — устройство везде сообщает UID из EEPROM, как донорский клон.
"""
import struct, hashlib

DIR = "/home/z/my-project/fw_analysis/"
ND = DIR + "new_dist/"
OUT = DIR + "OUTPUT/"

donor = open(DIR + "SM2_2.21.32_A111788_STM32F105VCT6.bin", "rb").read()      # 256КБ
stub = open(ND + "dec_sm2_a.bin", "rb").read()                                # 0xB00
app = open(ND + "dec_sm2_entry2.bin", "rb").read()                            # 0x1353C

FLASH_SIZE = 0x40000
STUB_BASE = 0x08004000
APP_BASE = 0x08005000

assert len(donor) == FLASH_SIZE
assert len(stub) == 0xB00
assert len(app) == 0x1353C

# ============================ 1. ПАТЧ ПРИЛОЖЕНИЯ ============================
PATCH_WORD_OLD = 0x1FFFF7E8   # адрес аппаратного UID STM32F105
PATCH_WORD_NEW = 0x080028E8   # адрес «виртуального UID» в EEPROM (данные донора)

patch_offs = []
app_patched = bytearray(app)
needle = struct.pack("<I", PATCH_WORD_OLD)
idx = 0
while True:
    idx = app.find(needle, idx)
    if idx < 0:
        break
    struct.pack_into("<I", app_patched, idx, PATCH_WORD_NEW)
    patch_offs.append(idx)
    idx += 4
print(f"Найдено и запатчено вхождений 0x{PATCH_WORD_OLD:08X}: {len(patch_offs)}")
for off in patch_offs:
    print(f"  flash 0x{APP_BASE+off:08X} (file+0x{off:X}): 0x{PATCH_WORD_OLD:08X} -> 0x{PATCH_WORD_NEW:08X}")
assert len(patch_offs) == 9, "Ожидалось ровно 9 вхождений!"
app_patched = bytes(app_patched)

# ============================ 2. СБОРКА ОБРАЗОВ ============================
def build(app_image):
    img = bytearray(b"\xFF" * FLASH_SIZE)
    img[0x00000:0x04000] = donor[0x00000:0x04000]        # бутлоадер + EEPROM донора
    img[0x04000:0x04000 + len(stub)] = stub              # stub 2.22.3
    img[0x05000:0x05000 + len(app_image)] = app_image    # основное приложение
    return bytes(img)

img_official = build(app)
img_patched = build(app_patched)

# ============================ 3. ВЕРИФИКАЦИЯ ============================
def rev32(x):
    return int("{:032b}".format(x)[::-1], 2)

def stm32_crc(data):
    crc = 0xFFFFFFFF
    for i in range(0, len(data), 4):
        w = rev32(struct.unpack_from("<I", data, i)[0])
        crc ^= w
        for _ in range(32):
            crc = ((crc << 1) ^ 0x04C11DB7) & 0xFFFFFFFF if crc & 0x80000000 else (crc << 1) & 0xFFFFFFFF
    return rev32(crc) ^ 0xFFFFFFFF

print()
print("=== ВЕРИФИКАЦИЯ ===")
for name, img, app_img, crc_exp in [
    ("restored (официальная)", img_official, app, 0x210E9A13),
    ("patched (патч клона)",  img_patched, app_patched, None),
]:
    print(f"--- {name} ---")
    sp, rst = struct.unpack_from("<II", img, 0)
    print(f"  Бутлоадер:  SP=0x{sp:08X} Reset=0x{rst:08X} {'OK' if sp == 0x20001800 and rst == 0x0800032D else 'FAIL'}")
    sp, rst = struct.unpack_from("<II", img, 0x4000)
    print(f"  Stub:       SP=0x{sp:08X} Reset=0x{rst:08X} {'OK' if sp == 0x20001830 and rst == 0x08004165 else 'FAIL'}")
    sp, rst = struct.unpack_from("<II", img, 0x5000)
    print(f"  Приложение: SP=0x{sp:08X} Reset=0x{rst:08X} {'OK' if sp == 0x2000FF30 and rst == 0x08005165 else 'FAIL'}")
    crc = stm32_crc(img[0x5000:0x5000 + len(app_img)])
    crc_st = stm32_crc(img[0x4000:0x4000 + len(stub)])
    print(f"  CRC stub: 0x{crc_st:08X} {'OK (== 0x2912D0A0)' if crc_st == 0x2912D0A0 else 'FAIL'}")
    if crc_exp:
        print(f"  CRC приложения: 0x{crc:08X} {'OK (== 0x210E9A13 из драйвера)' if crc == crc_exp else 'FAIL'}")
    else:
        print(f"  CRC приложения (патченного): 0x{crc:08X} (официальный 0x210E9A13 — изменение ожидаемо)")
    marker = struct.unpack_from("<H", img, 0x2FFE)[0]
    print(f"  Маркер EEPROM стр.1: 0x{marker:04X} {'OK' if marker == 0x5AA5 else 'FAIL'}")
    serial = struct.unpack_from("<I", img, 0x180)[0]
    print(f"  Серийный номер: 0x{serial:08X} = {serial:07X}")
    w = struct.unpack_from("<I", img, 0x28E8)[0]
    b = img[0x28F3]
    print(f"  Виртуальный UID в EEPROM: слово 0x{w:08X} {'OK' if w == 0x3247F69E else 'FAIL'}, байт 0x{b:02X} {'OK' if b == 0x43 else 'FAIL'}")
    n_uid = sum(1 for off in patch_offs if struct.unpack_from('<I', img, 0x5000+off)[0] == PATCH_WORD_NEW)
    print(f"  Патченных слов в образе: {n_uid}/9")
    print(f"  MD5:    {hashlib.md5(img).hexdigest()}")
    print(f"  SHA256: {hashlib.sha256(img).hexdigest()}")
    print()

# ============================ 4. СОХРАНЕНИЕ ============================
open(OUT + "SM2Pro_full_flash_2.22.3_restored.bin", "wb").write(img_official)
open(OUT + "SM2Pro_full_flash_2.22.3_patched.bin", "wb").write(img_patched)
open(OUT + "SM2_2.22.3_stub.bin", "wb").write(stub)
open(OUT + "SM2_2.22.3_app_official.bin", "wb").write(app)
open(OUT + "SM2_2.22.3_app_patched.bin", "wb").write(app_patched)
print("Сохранено в OUTPUT:")
print("  SM2Pro_full_flash_2.22.3_restored.bin (256КБ, официальное приложение)")
print("  SM2Pro_full_flash_2.22.3_patched.bin   (256КБ, патч клона — аналог донорского)")
print("  SM2_2.22.3_stub.bin                    (0xB00, грузить по 0x08004000)")
print("  SM2_2.22.3_app_official.bin            (0x1353C, грузить по 0x08005000)")
print("  SM2_2.22.3_app_patched.bin             (0x1353C, грузить по 0x08005000)")
