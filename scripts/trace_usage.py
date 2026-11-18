#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Полный анализ использования слова 0x0800E958: вызовы, хелперы, другие ссылки на UID."""
from capstone import *
import struct, re

DIR = "/home/z/my-project/fw_analysis/"
donor = open(DIR + "SM2_2.21.32_A111788_STM32F105VCT6.bin", "rb").read()
official = open(DIR + "SM2Pro_full_flash_2.21.32_restored.bin", "rb").read()
FLASH_BASE = 0x08000000
md = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_MCLASS)
md.detail = True

FUNCS = [0x0800E764, 0x0800E814]  # функции, использующие пул с нашим словом

# ---------- 1. Кто вызывает 0x0800E764 / 0x0800E814 (BL) и табличные ссылки ----------
print("=== 1. Вызовы (BL) функций 0x0800E764 / 0x0800E814 в приложении ===")
for target in FUNCS:
    hits = []
    for pos in range(0x04000, 0x0F2E0 - 4, 2):
        hw = struct.unpack_from("<H", donor, pos)[0]
        if (hw & 0xF800) == 0xF000:  # BL prefix
            hw2 = struct.unpack_from("<H", donor, pos + 2)[0]
            if (hw2 & 0xD000) == 0xD000:  # BL suffix
                S = (hw >> 10) & 1
                imm10 = hw & 0x3FF
                J1 = (hw2 >> 13) & 1
                J2 = (hw2 >> 11) & 1
                imm11 = hw2 & 0x7FF
                I1 = (~(J1 ^ S)) & 1
                I2 = (~(J2 ^ S)) & 1
                off = (S << 24) | (I1 << 23) | (I2 << 22) | (imm10 << 12) | (imm11 << 1)
                if S:
                    off |= 0xFE000000
                    off -= 0x100000000
                pc = FLASH_BASE + pos + 4
                tgt = (pc + off) & 0xFFFFFFFF
                if tgt == target:
                    hits.append(FLASH_BASE + pos)
    print(f"  0x{target:08X} вызывается из: " + (", ".join(f"0x{h:08X}" for h in hits) if hits else "(нет прямых BL)"))

# Табличные ссылки (слово = адрес|1)
print("\n=== Табличные ссылки (слова 0x0800E765/0x0800E815) в приложении ===")
for target in FUNCS:
    needle = struct.pack("<I", target | 1)
    idx = 0x04000
    while True:
        idx = donor.find(needle, idx, 0x0F2E0)
        if idx < 0: break
        print(f"  0x{target:08X}|1 найдено по адресу 0x{FLASH_BASE+idx:08X}")
        idx += 4

# ---------- 2. Хелперы ----------
print("\n=== 2. Дизассемблировка хелперов ===")
def disasm(data, start, end, note=""):
    print(f"--- 0x{FLASH_BASE+start:08X}..0x{FLASH_BASE+end:08X} {note} ---")
    for ins in md.disasm(data[start:end], FLASH_BASE + start):
        print(f"  0x{ins.address:08X}: {ins.bytes.hex():<12} {ins.mnemonic:<9} {ins.op_str}")
    print()

# 0x0800BAA8, 0x0800BAC8, 0x0800BADC, 0x0800BA92, 0x0800BA7C, 0x0800E6F8
disasm(donor, 0x0BA7C, 0x0BB40, "хелперы 0x0800BA7C-0x0800BB40")

# ---------- 3. Другие вхождения значений 0x1FFFF7E8 / 0x080028E8 ----------
print("=== 3. Слова 0x1FFFF7E8 / 0x080028E8 во всём дампе (донор и официальный) ===")
for name, data in [("донор", donor), ("официальный", official)]:
    for val in (0x1FFFF7E8, 0x080028E8):
        needle = struct.pack("<I", val)
        idx = 0
        hits = []
        while True:
            idx = data.find(needle, idx, 0x10000)
            if idx < 0: break
            hits.append(FLASH_BASE + idx)
            idx += 4
        print(f"  {name}: 0x{val:08X} -> " + (", ".join(f"0x{h:08X}" for h in hits) if hits else "(нет)"))

# ---------- 4. MOVW/MOVT, создающие 0x1FFF / 0xF7E8 / 0x0800 / 0x28E8 ----------
print("\n=== 4. MOVW/MOVT пары (capstone) для 0x1FFFF7E8/0x080028E8 в приложении (обе версии) ===")
for name, data in [("донор", donor), ("официальный", official)]:
    last_mov = {}  # reg -> (addr, imm)
    for ins in md.disasm(data[0x04000:0x0F2E0], FLASH_BASE + 0x04000):
        if ins.mnemonic == "movw":
            m = re.match(r"r(\d+), #0x([0-9a-f]+)", ins.op_str.replace(" ", ""))
            if m:
                last_mov[int(m.group(1))] = (ins.address, int(m.group(2), 16))
        elif ins.mnemonic == "movt":
            m = re.match(r"r(\d+), #0x([0-9a-f]+)", ins.op_str.replace(" ", ""))
            if m:
                r = int(m.group(1))
                if r in last_mov:
                    full = (int(m.group(2), 16) << 16) | last_mov[r][1]
                    if full in (0x1FFFF7E8, 0x080028E8):
                        print(f"  {name}: 0x{last_mov[r][0]:08X} movw + 0x{ins.address:08X} movt -> r{r} = 0x{full:08X}")
