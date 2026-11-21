#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Поиск зашитых образов STM32 в файлах драйвера."""
import os, struct, re

DRIVER = "/home/z/my-project/fw_analysis/driver/Scanmatik"
# Первые 8 байт приложения из нашего дампа (SP=0x2000FD60, Reset=0x08004169)
APP_SIG = bytes.fromhex("60FD002069410008")
# Первые 8 байт бутлоадера (SP=0x20001800, Reset=0x0800032D)
BL_SIG = bytes.fromhex("001820002D030008")

print("=== Поиск сигнатур прошивки ===")
files = []
for root, dirs, fs in os.walk(DRIVER):
    for f in sorted(fs):
        files.append(os.path.join(root, f))

for p in files:
    try:
        d = open(p, "rb").read()
    except:
        continue
    for name, sig in [("APP(0x08004000)", APP_SIG), ("BOOTLOADER", BL_SIG)]:
        for m in re.finditer(re.escape(sig), d):
            print(f"  {os.path.basename(p)}: {name} @ file offset 0x{m.start():X}")

print()
print("=== Поиск通用 векторных таблиц STM32 (SP в RAM + reset thumb во flash) ===")
for p in files:
    if os.path.getsize(p) > 60_000_000: continue
    try:
        d = open(p, "rb").read()
    except:
        continue
    found = []
    for off in range(0, len(d) - 0x40, 4):
        w0, w1 = struct.unpack_from("<II", d, off)
        if 0x20000100 <= w0 <= 0x20010000 and (w0 & 7) == 0:
            if 0x08000001 <= w1 <= 0x08040000 and (w1 & 1) == 1:
                # Проверим ещё пару векторов
                ok = True
                for k in range(2, 8):
                    v = struct.unpack_from("<I", d, off + 4*k)[0]
                    if not (v == 0 or (0x08000001 <= v <= 0x08040000 and v & 1) or v == 0xFFFFFFFF):
                        ok = False; break
                if ok:
                    found.append(off)
    if found:
        print(f"  {os.path.basename(p)}: {len(found)} кандидатов @ {[hex(x) for x in found[:15]]}")
