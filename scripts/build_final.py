#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Финальная сборка восстановительного дампа SM2Pro (STM32F105VCT6, 256KB).

Карта флеша:
  0x08000000-0x08002FFF  бутлоадер (код)          <- из референс-дампа (проверен)
  0x08002800-0x08002FFF  EEPROM стр.1 (настройки) <- из референс-дампа
  0x08003000-0x080037FF  EEPROM стр.2 (пусто)     <- из референс-дампа
  0x08004000-0x0800F2DF  приложение 2.21.32       <- ОФИЦИАЛЬНЫЙ образ из sm2lib.dll (CRC OK)
  0x0800F2E0-0x0800F7FF  заводские данные         <- из референс-дампа
  0x0800F800-0x0803FFFF  пусто (0xFF)
"""
import struct, hashlib

DIR = "/home/z/my-project/fw_analysis/"
ref = open(DIR + "SM2_2.21.32_A111788_STM32F105VCT6.bin", "rb").read()          # 256KB референс
app_official = open(DIR + "app_sm2_2.21.32_decrypted.bin", "rb").read()          # 0xB2E0 официальное приложение

FLASH_SIZE = 0x40000  # 256KB STM32F105VCT6

assert len(ref) == FLASH_SIZE
assert len(app_official) == 0xB2E0

# === Сборка ===
img = bytearray(b"\xFF" * FLASH_SIZE)

# 1. Бутлоадер + EEPROM обе страницы: 0x00000-0x03FFF из референса
img[0x00000:0x04000] = ref[0x00000:0x04000]

# 2. Приложение: официальный образ из драйвера 0x04000-0x0F2E0
img[0x04000:0x04000 + len(app_official)] = app_official

# 3. Заводской хвост: 0x0F2E0-0x0F800 из референса (данные не пишутся апдейтером)
img[0x0F2E0:0x0F800] = ref[0x0F2E0:0x0F800]

# 4. 0x0F800-0x3FFF уже 0xFF

out = DIR + "SM2Pro_full_flash_2.21.32_restored.bin"
open(out, "wb").write(img)

# === Верификация ===
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

print("=== ВЕРИФИКАЦИЯ ВОССТАНОВЛЕННОГО ДАМПА ===")
sp, rst = struct.unpack_from("<II", img, 0)
print(f"Бутлоадер: SP=0x{sp:08X} Reset=0x{rst:08X} {'OK' if sp == 0x20001800 else 'FAIL'}")
sp2, rst2 = struct.unpack_from("<II", img, 0x4000)
print(f"Приложение: SP=0x{sp2:08X} Reset=0x{rst2:08X} {'OK' if sp2 == 0x2000FD60 else 'FAIL'}")
crc = stm32_crc(img[0x4000:0x4000 + 0xB2E0])
print(f"CRC32 приложения: 0x{crc:08X} {'OK (== 0xBDEE4E94 из драйвера)' if crc == 0xBDEE4E94 else 'FAIL'}")
marker = struct.unpack_from("<H", img, 0x2FFE)[0]
print(f"EEPROM маркер стр.1 (0x2FFE): 0x{marker:04X} {'OK' if marker == 0x5AA5 else 'FAIL'}")
serial = struct.unpack_from("<I", img, 0x180)[0]
print(f"Серийный номер (0x08000180): 0x{serial:08X} = {serial:07X}")
print(f"Размер: {len(img)} байт ({len(img)//1024} КБ)")
print()
print(f"MD5:    {hashlib.md5(img).hexdigest()}")
print(f"SHA256: {hashlib.sha256(img).hexdigest()}")

# Альтернатива: донорский дамп как есть
open(DIR + "SM2Pro_full_flash_2.21.32_donor_asis.bin", "wb").write(ref)
print()
print(f"Донорский дамп (как есть):   MD5 {hashlib.md5(ref).hexdigest()}")

# Чистое приложение для частичной прошивки/отладки
print(f"Официальное приложение:      MD5 {hashlib.md5(app_official).hexdigest()}")

# Карта заполнения
print()
print("Карта заполнения (2КБ страницы, X=данные, .=0xFF):")
for i in range(0, FLASH_SIZE, 2048):
    chunk = img[i:i+2048]
    c = "." if all(b == 0xFF for b in chunk) else ("0" if all(b == 0 for b in chunk) else "X")
    if i % (2048 * 32) == 0:
        print(f"\n  0x{0x08000000+i:06X}: ", end="")
    print(c, end="")
print()
