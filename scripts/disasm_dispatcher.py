#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Дизассемблирование FUN_080010aa (диспетчер команд) для поиска jump table."""
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
        print(f"  0x{ins.address:08X}: {ins.bytes.hex():<12} {ins.mnemonic:<9} {ins.op_str}")
    print()

disasm(0x080010AA, 0x120, "FUN_080010aa dispatcher")
# jump table находится после функции — посмотрим литералы
print("--- Слова 0x080011B0-0x080011C8 ---")
for a in range(0x080011B0, 0x080011C8, 4):
    w = struct.unpack_from("<I", data, a - FLASH_BASE)[0]
    print(f"  0x{a:08X}: 0x{w:08X}")
print()
# FUN_08000ea2 - что делает перед прыжком в системный загрузчик
disasm(0x08000EA2, 0x1C, "FUN_08000ea2")
