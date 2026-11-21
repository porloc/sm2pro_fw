#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Сборка v3: минимальный UID-патч (только auth-пул 0x0800C520).

Диагностика ошибки «Внутренняя ошибка микропрограммы 00000»:
- v2 (патч всех 9 слов UID) → приложение стартует, но ПК-программа получает
  ошибку с кодом 0x00000 на ПОСЛЕ-запусковом обмене.
- Гипотеза A: чрезмерный патч (9 слов) ломает не-auth кодовые пути 2.22.3.
- Гипотеза B: приложение не отвечает из-за несовместимости со старым
  бутлоадером / отсутствия новых данных (0x8B / конфиг-слоты).

v3 изолирует гипотезу A: патчим ТОЛЬКО пул 0x0800C520 (функция 0x0800C15C —
ядро аутентификации cmd 0x12, прямой аналог слова 0x0800E958 в 2.21.32).
Остальные 8 слов остаются 0x1FFFF7E8 (аппаратный UID).
"""
import struct, hashlib

SRC = "/home/z/my-project/fw_analysis/OUTPUT/SM2Pro_full_flash_2.22.3_patched_v2.bin"
OUT = "/home/z/my-project/fw_analysis/OUTPUT/SM2Pro_full_flash_2.22.3_patched_v3_minimal.bin"

data = bytearray(open(SRC, "rb").read())
assert len(data) == 0x40000

BASE = 0x08000000
AUTH_POOL = 0x0800C520          # пул литералов auth-функции 0x0800C15C
ORIG = 0x1FFFF7E8               # адрес аппаратного UID
VIRT = 0x080028E8               # виртуальный UID в EEPROM (донор)

# все слова, которые в v2 были заменены (для контроля)
patched_v2 = [0x0800C520, 0x0800D5C8, 0x0800D998, 0x0800DD7C, 0x0800E15C,
              0x0800E700, 0x0800EACC, 0x0800EEA4, 0x0800F950]

changed = 0
# вернуть все, КРОМЕ auth-пула, к оригиналу 0x1FFFF7E8
for addr in patched_v2:
    off = addr - BASE
    cur = struct.unpack_from("<I", data, off)[0]
    if addr == AUTH_POOL:
        if cur != VIRT:
            raise RuntimeError(f"v2: пул 0x{addr:08X} = 0x{cur:08X}, ожидался 0x{VIRT:08X}")
        # оставляем патч
    else:
        if cur != VIRT:
            raise RuntimeError(f"v2: пул 0x{addr:08X} = 0x{cur:08X}, ожидался 0x{VIRT:08X}")
        struct.pack_into("<I", data, off, ORIG)
        changed += 1

open(OUT, "wb").write(bytes(data))
print(f"OK: {OUT}")
print(f"  возвращено к 0x{ORIG:08X}: {changed} слов (пулы кроме 0x{AUTH_POOL:08X})")
print(f"  оставлен патч 0x{ORIG:08X} -> 0x{VIRT:08X}: пул 0x{AUTH_POOL:08X}")
print(f"  размер: {len(data)} (0x{len(data):X})")

md5 = hashlib.md5(bytes(data)).hexdigest()
sha = hashlib.sha256(bytes(data)).hexdigest()
print(f"  MD5:    {md5}")
print(f"  SHA256: {sha}")

# контроль: разница с официальным приложением — ровно 1 слово
off_app = "/home/z/my-project/fw_analysis/OUTPUT/SM2Pro_full_flash_2.22.3_official_v2.bin"
ref = open(off_app, "rb").read()
diffs = [i for i in range(len(data)) if data[i] != ref[i]]
print(f"  различий с official_v2: {len(diffs)} байт (ожидалось 3 — одно слово)")
