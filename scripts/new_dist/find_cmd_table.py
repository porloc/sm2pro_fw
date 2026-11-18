#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Поиск таблицы команд в новом приложении 2.22.3 (base 0x08005000)."""
import struct

app = open("/home/z/my-project/fw_analysis/new_dist/dec_sm2_entry2.bin", "rb").read()
BASE = 0x08005000
SIZE = len(app)

# Сканируем: таблица команд {code:1, flags:1, pad:2, handler:4} — handler = thumb ptr в пределах app
# Ищем серии из >= 8 записей подряд, где handler валиден и code возрастает/уникален
best = []
for off in range(0, SIZE - 8, 4):
    n = 0
    codes = []
    while off + n * 8 + 8 <= SIZE:
        code, flags = struct.unpack_from("<BB", app, off + n * 8)
        pad, handler = struct.unpack_from("<HI", app, off + n * 8 + 2)
        if not (BASE + 1 <= handler <= BASE + SIZE) or (handler & 1) == 0:
            break
        if pad != 0:
            break
        codes.append((code, flags, handler))
        n += 1
    if n >= 8:
        best.append((off, n, codes))

for off, n, codes in best:
    uniq = len(set(c for c, f, h in codes))
    print(f"Таблица @ 0x{BASE+off:08X}: {n} записей, уникальных кодов {uniq}")
    if uniq >= n * 0.7:
        for c, f, h in codes:
            print(f"    код 0x{c:02X} флаги 0x{f:02X} -> 0x{h:08X}")
        print()
