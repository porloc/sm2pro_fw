#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Дизассемблирование stub (entry1, 0xB00 @ 0x08004000) из прошивки 2.22.3."""
from capstone import *
import struct

md = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_MCLASS)
md.detail = False

stub = open("/home/z/my-project/fw_analysis/new_dist/dec_sm2_a.bin", "rb").read()
BASE = 0x08004000

# Векторная таблица
print("=== Векторы stub ===")
n_vec = 0
for i in range(0, 0x100, 4):
    v = struct.unpack_from("<I", stub, i)[0]
    if v == 0xFFFFFFFF or v == 0:
        n_vec = i
        break
    print(f"  [{i//4}] 0x{v:08X}")
print()

# Код после векторов
print("=== Код stub (полный дизассемблерный проход) ===")
for ins in md.disasm(stub[0x100:], BASE + 0x100):
    print(f"  0x{ins.address:08X}: {ins.bytes.hex():<10} {ins.mnemonic:<9} {ins.op_str}")
