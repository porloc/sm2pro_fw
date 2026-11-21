#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Дизассемблирование ключевых функций бутлоадера."""
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
        # Подсветка вызовов/переходов
        extra = ""
        if ins.mnemonic in ("bl", "blx", "b", "bx") :
            try:
                t = int(ins.op_str.lstrip('#'), 16) if ins.op_str.startswith('#') else None
            except: t = None
            if t: extra = f"  -> 0x{t:08X}"
        print(f"  0x{ins.address:08X}: {ins.bytes.hex():<12} {ins.mnemonic:<9} {ins.op_str}{extra}")
    print()

disasm(0x08002660, 0xA2, "FUN_08002660 (startup/init)")
disasm(0x08001338, 0xC0, "FUN_08001338 (main?)")
