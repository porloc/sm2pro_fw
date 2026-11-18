#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Поиск зашифрованной прошивки: энтропия + ресурсы sm2lib.dll и других."""
import pefile, collections, math, os, re

DIR = "/home/z/my-project/fw_analysis/driver/Scanmatik"

def entropy(b):
    if not b: return 0
    c = collections.Counter(b)
    return -sum(n/len(b)*math.log2(n/len(b)) for n in c.values())

def scan_file(path):
    d = open(path, 'rb').read()
    # высокоэнтропийные блоки 4КБ, объединённые в регионы > 32КБ
    hi = []
    for i in range(0, len(d) - 0x1000, 0x1000):
        if entropy(d[i:i+0x1000]) > 7.0:
            hi.append(i)
    if not hi: return []
    regions = []
    start = prev = hi[0]
    for h in hi[1:]:
        if h - prev > 0x1000:
            regions.append((start, prev+0x1000))
            start = h
        prev = h
    regions.append((start, prev+0x1000))
    return [(s, e) for s, e in regions if e - s >= 0x8000]

for f in sorted(os.listdir(DIR)):
    if not f.endswith(('.dll', '.exe')): continue
    p = os.path.join(DIR, f)
    regs = scan_file(p)
    if regs:
        print(f"{f} ({os.path.getsize(p)}):")
        for s, e in regs:
            print(f"   регион 0x{s:X}-0x{e:X} ({(e-s)//1024} КБ, ent={entropy(open(p,'rb').read()[s:e]):.2f})")

# Ресурсы sm2lib.dll
print()
print("=== Ресурсы sm2lib.dll ===")
pe = pefile.PE(os.path.join(DIR, "sm2lib.dll"))
if hasattr(pe, 'DIRECTORY_ENTRY_RESOURCE'):
    for rt in pe.DIRECTORY_ENTRY_RESOURCE.entries:
        for rid in rt.directory.entries:
            for rlang in rid.directory.entries:
                sz = rlang.data.struct.Size
                print(f"  Type={rt.id if rt.name is None else rt.name} ID={rid.id if rid.name is None else rid.name} Size={sz}")
                data = pe.get_data(rlang.data.struct.OffsetToData, min(sz, 64))
                print(f"    head: {data.hex()}")
