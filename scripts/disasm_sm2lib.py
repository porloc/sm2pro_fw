#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Дизассемблирование кода sm2lib.dll вокруг ссылок на блоб прошивки."""
from capstone import *
import struct

path = "/home/z/my-project/fw_analysis/driver/Scanmatik/sm2lib.dll"
d = open(path, "rb").read()
md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = False

# file offset -> VA: .text VA=0x1000 Raw=0x400, ImageBase=0x10000000
def file_to_va(off):
    if off >= 0x400 and off < 0x3A200:  # .text
        return 0x10000000 + 0x1000 + (off - 0x400)
    elif off >= 0x3A200 and off < 0x64E00:  # .rdata
        return 0x10000000 + 0x3B000 + (off - 0x3A200)
    return None

def disasm_range(fstart, fend, title):
    va = file_to_va(fstart)
    print(f"--- {title}: file 0x{fstart:X}-0x{fend:X} (VA 0x{va:08X}+) ---")
    code = d[fstart:fend]
    for ins in md.disasm(code, va):
        print(f"  0x{ins.address:08X}: {ins.bytes.hex():<20} {ins.mnemonic:<8} {ins.op_str}")
    print()

disasm_range(0xA380, 0xA5C0, "Код вокруг ссылок на блоб (0xA3AD, 0xA4EE)")
