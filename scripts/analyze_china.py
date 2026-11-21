#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Глубокий анализ china.dll: поиск образов прошивки в .rdata."""
import pefile, struct, collections, math, re

path = "/home/z/my-project/fw_analysis/driver/Scanmatik/china.dll"
pe = pefile.PE(path)
for s in pe.sections:
    if s.Name.decode().rstrip(chr(0)) == '.rdata':
        data = s.get_data()
        break
print(f".rdata: {len(data)} байт")

def entropy(b):
    if not b: return 0
    c = collections.Counter(b)
    return -sum(n/len(b)*math.log2(n/len(b)) for n in c.values())

# 1. Карта энтропии по 8КБ блокам
print("=== Карта энтропии (блоки 8КБ) ===")
high_regions = []
for i in range(0, len(data), 0x2000):
    chunk = data[i:i+0x2000]
    e = entropy(chunk)
    if e > 7.2:
        high_regions.append(i)
print(f"Блоков с энтропией >7.2: {len(high_regions)} из {len(data)//0x2000}")
if high_regions:
    # Объединение в регионы
    regions = []
    start = high_regions[0]
    prev = high_regions[0]
    for h in high_regions[1:]:
        if h - prev > 0x2000:
            regions.append((start, prev+0x2000))
            start = h
        prev = h
    regions.append((start, prev+0x2000))
    print("Высокоэнтропийные регионы:")
    for r in regions:
        print(f"  0x{r[0]:X} - 0x{r[1]:X} ({(r[1]-r[0])//1024} КБ, entropy={entropy(data[r[0]:r[1]]):.2f})")

# 2. Поиск STM32 векторных таблиц по всему файлу china.dll
print()
print("=== Поиск STM32 VT во всём china.dll ===")
whole = open(path, 'rb').read()
for off in range(0, len(whole) - 0x40, 4):
    w0, w1 = struct.unpack_from("<II", whole, off)
    if 0x20000100 <= w0 <= 0x20010000 and (w0 & 7) == 0:
        if 0x08000001 <= w1 <= 0x08040000 and (w1 & 1) == 1:
            ok = True
            for k in range(2, 8):
                v = struct.unpack_from("<I", whole, off + 4*k)[0]
                if not (v == 0 or (0x08000001 <= v <= 0x08040000 and v & 1) or v == 0xFFFFFFFF):
                    ok = False; break
            if ok:
                print(f"  file+0x{off:X}: SP=0x{w0:08X} Reset=0x{w1:08X}")

# 3. Строки в china.dll про firmware/update/версии
print()
print("=== Строки china.dll (utf-16 и ascii) про firmware ===")
for m in re.finditer(rb'(?:[\x20-\x7e]\x00){5,}', whole):
    s = m.group().decode('utf-16-le', 'ignore')
    if re.search(r'(?i)firmware|update|flash|loader|\.bin|stm32|version|dump|proshiv', s):
        print(f"  [U16 @0x{m.start():X}] {s[:100]}")
for m in re.finditer(rb'[\x20-\x7e]{8,}', whole):
    s = m.group().decode('ascii', 'ignore')
    if re.search(r'(?i)firmware|update|\.bin|stm32|loader', s):
        print(f"  [ASC @0x{m.start():X}] {s[:100]}")
