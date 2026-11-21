#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Поиск крипто-констант бутлоадера и образов прошивки в файлах драйвера."""
import os, struct, re

DRIVER = "/home/z/my-project/fw_analysis/driver/Scanmatik"

K1 = struct.pack("<I", 0x13AB3377)
K2 = struct.pack("<I", 0x5188016B)
A0 = struct.pack("<I", 0xCAFE1381)
# Дополнительно: константы из бинарника в целом
SERIAL = struct.pack("<I", 0x0A111788)

print("=== Поиск крипто-констант протокола обновления SM2 ===")
for root, dirs, files in os.walk(DRIVER):
    for f in sorted(files):
        p = os.path.join(root, f)
        try:
            d = open(p, "rb").read()
        except:
            continue
        hits = []
        for name, pat in [("K1=0x13AB3377", K1), ("K2=0x5188016B", K2), ("A0=0xCAFE1381", A0), ("SERIAL", SERIAL)]:
            idx = [m.start() for m in re.finditer(re.escape(pat), d)]
            if idx:
                hits.append(f"{name} x{len(idx)} @ {[hex(i) for i in idx[:6]]}")
        if hits:
            print(f"  {f}:")
            for h in hits:
                print(f"     {h}")
