#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Дамп таблицы функций 0x080002B0-0x08000350 и поиск вызовов FUN_08000f3e."""
import struct
from capstone import *

BIN = "/home/z/my-project/fw_analysis/SM2_2.21.32_A111788_STM32F105VCT6.bin"
FLASH_BASE = 0x08000000
data = open(BIN, "rb").read()
md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)

print("=== Таблица/литералы 0x080002B0-0x08000354 ===")
for a in range(0x080002B0, 0x08000354, 4):
    off = a - FLASH_BASE
    w = struct.unpack_from("<I", data, off)[0]
    note = ""
    if 0x08000001 <= w <= 0x08003000 and w & 1:
        note = f"  → thumb func 0x{w-1:08X}"
    elif 0x08000001 <= w <= 0x08003000:
        note = f"  → 0x{w:08X}"
    print(f"  0x{a:08X}: 0x{w:08X}{note}")

print()
print("=== Все BL/B.W в бутлоадере на цели 0x08000F3x-0x08000F4x ===")
for ins in md.disasm(data[0:0x2800], FLASH_BASE):
    if ins.mnemonic in ("bl", "b.w", "b") and ("0x8000f3" in ins.op_str or "0x8000f4" in ins.op_str):
        print(f"  {ins.mnemonic} @ 0x{ins.address:08X} → {ins.op_str}")

print()
print("=== Кто пишет в 0x200000BC (state) / ссылки на 0x200000B0 ===")
# Поиск литералов со значением 0x200000B0
for off in range(0, 0x2800, 2):
    w = struct.unpack_from("<I", data, off)[0]
    if 0x200000A0 <= w <= 0x200000D0:
        print(f"  литерал 0x{FLASH_BASE+off:08X} = 0x{w:08X}")
