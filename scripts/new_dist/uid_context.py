#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Дизассемблирование функций, использующих UID (0x1FFFF7E8) в новом приложении."""
from capstone import *
import struct

md = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_MCLASS)
app = open("/home/z/my-project/fw_analysis/new_dist/dec_sm2_entry2.bin", "rb").read()
BASE = 0x08005000

# (сайт загрузки литерала, пул)
SITES = [
    (0x0800C15E, 0x0800C520), (0x0800C46E, 0x0800C520),
    (0x0800D204, 0x0800D5C8), (0x0800D5C0, 0x0800D5C8),
    (0x0800D682, 0x0800D998),
    (0x0800DD50, 0x0800DD7C),
    (0x0800E068, 0x0800E15C),
    (0x0800E364, 0x0800E700),
    (0x0800E7B4, 0x0800EACC),
    (0x0800ECDC, 0x0800EEA4), (0x0800EE4E, 0x0800EEA4),
    (0x0800F5A8, 0x0800F950),
]

for site, pool in SITES:
    start = site - BASE - 0x50
    end = site - BASE + 0xA0
    print(f"=== Сайт 0x{site:08X} (пул 0x{pool:08X}) ===")
    for ins in md.disasm(app[start:end], BASE + start):
        mark = ""
        if ins.address <= site < ins.address + ins.size:
            mark = "   <<<< UID LOAD"
        print(f"  0x{ins.address:08X}: {ins.bytes.hex():<10} {ins.mnemonic:<9} {ins.op_str}{mark}")
    print()
