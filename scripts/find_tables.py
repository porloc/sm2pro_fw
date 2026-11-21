#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Поиск таблиц указателей на функции-обёртки 0x0800122a+ и анализ USB транспорта."""
import struct
from capstone import *

BIN = "/home/z/my-project/fw_analysis/SM2_2.21.32_A111788_STM32F105VCT6.bin"
FLASH_BASE = 0x08000000
data = open(BIN, "rb").read()

# 1. Поиск ссылок (как данных) на функции 0x0800122a..0x080012e4 (thumb-указатели)
targets = [0x0800122a, 0x0800123a, 0x08001248, 0x0800125a, 0x0800126a, 0x08001286, 0x08001298, 0x080012a8, 0x080012e4]
print("=== Поиск thumb-указателей на функции-обёртки ===")
found = []
for off in range(0, len(data)-4, 2):
    w = struct.unpack_from("<I", data, off)[0]
    if w in [t|1 for t in targets] or w in targets:
        print(f"  0x{FLASH_BASE+off:08X}: 0x{w:08X}")
        found.append(off)

# 2. Поиск BL на FUN_08000f3e (erase)
print()
print("=== Поиск BL → FUN_08000f3e (0x08000F3E) ===")
md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
for ins in md.disasm(data[0:0x2800], FLASH_BASE):
    if ins.mnemonic == "bl" and "0x8000f3e" in ins.op_str:
        print(f"  BL @ 0x{ins.address:08X}")

# 3. Дизассемблирование FUN_08001708 (получить запрос) и FUN_08001784 (отправить ответ)
def disasm(addr, size, title=""):
    off = addr - FLASH_BASE
    print(f"--- {title} @ 0x{addr:08X} ---")
    for ins in md.disasm(data[off:off+size], addr):
        print(f"  0x{ins.address:08X}: {ins.bytes.hex():<12} {ins.mnemonic:<9} {ins.op_str}")
    print()

disasm(0x08001708, 0x38, "FUN_08001708 (получить пакет)")
disasm(0x08001784, 0x20, "FUN_08001784 (отправить ответ)")
disasm(0x08001750, 0x40, "FUN_08001750/FUN_08001740")
