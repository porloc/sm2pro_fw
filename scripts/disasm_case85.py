#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Дизассемблирование обработчика case 0x85 и USB-функций."""
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

disasm(0x0800119C, 0x30, "case 0x85 handler (ERASE?)")
disasm(0x08000EA2, 0x40, "FUN_08000ea2")
