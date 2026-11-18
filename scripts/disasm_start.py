#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Дизассемблирование стартового кода бутлоадера 0x08000204+."""
from capstone import *
import struct

BIN = "/home/z/my-project/fw_analysis/SM2_2.21.32_A111788_STM32F105VCT6.bin"
FLASH_BASE = 0x08000000
data = open(BIN, "rb").read()

md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)

def disasm(addr, size, title=""):
    off = addr - FLASH_BASE
    print(f"--- {title} @ 0x{addr:08X} ---")
    for ins in md.disasm(data[off:off+size], addr):
        print(f"  0x{ins.address:08X}: {ins.bytes.hex():<10} {ins.mnemonic:<8} {ins.op_str}")
    print()

# Цель reset handler
disasm(0x08000204, 0x14, "Reset target (0x08000204)")

# Слова после векторной таблицы — как данные
print("--- Слова 0x08000118-0x08000204 (хвост VT + данные) ---")
for a in range(0x08000118, 0x08000204, 4):
    off = a - FLASH_BASE
    w = struct.unpack_from("<I", data, off)[0]
    print(f"  0x{a:08X}: 0x{w:08X}")
print()

# thunk на 0x0800020c
disasm(0x0800020C, 0xC, "thunk @ 0x0800020c")
# FUN_08000218 - SVC handler?
disasm(0x08000218, 0xB4, "FUN_08000218 (context switch?)")
