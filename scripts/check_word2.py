#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Строгий поиск всех ссылок на слово 0x0800E958 во всём дампе (донор)."""
from capstone import *
from capstone.arm import *
import struct

DIR = "/home/z/my-project/fw_analysis/"
donor = open(DIR + "SM2_2.21.32_A111788_STM32F105VCT6.bin", "rb").read()

FLASH_BASE = 0x08000000
WORD_ADDR = 0x0800E958

# ---------- 0. Байтовый дамп области ----------
print("=== Байты 0x0800E930..0x0800E980 (донор) ===")
for off in range(0x0E930, 0x0E980, 16):
    row = donor[off:off+16]
    print(f"0x{FLASH_BASE+off:08X}: " + " ".join(f"{b:02X}" for b in row))
print()

# ---------- 1. Линейный скан всех PC-относительных LDR литералов ----------
# Идём по коду приложения (0x08004000..0x0800F2E0) и бутлоадера (0x08000204..0x08002800),
# ищем 16-бит LDR Rt,[PC,#imm8*4] (0x48xx-0x4Fxx) и 32-bit LDR.W Rt,[PC,#imm12] (F8DF)
def scan_literal_loads(data, regions):
    refs = {}  # target -> list of (addr, insn)
    for (start_off, end_off) in regions:
        # перебираем каждое 2-байтовое смещение (код может быть не выровнен)
        pos = start_off
        while pos < end_off - 1:
            hw = struct.unpack_from("<H", data, pos)[0]
            # 16-bit LDR literal: 0100 1 Rt(3) imm8
            if (hw & 0xF800) == 0x4800:
                rt = (hw >> 8) & 7
                imm = (hw & 0xFF) * 4
                pc = (FLASH_BASE + pos + 4) & ~3
                tgt = pc + imm
                refs.setdefault(tgt, []).append((FLASH_BASE + pos, f"ldr r{rt}, [pc, #0x{imm:x}]"))
                pos += 2
                continue
            # 32-bit LDR.W literal: F8DF F000-ish: 1111 1000 1101 1111 Rt imm12
            if hw == 0xF8DF:
                hw2 = struct.unpack_from("<H", data, pos+2)[0]
                rt = (hw2 >> 12) & 0xF
                imm = hw2 & 0xFFF
                pc = (FLASH_BASE + pos + 4) & ~3
                tgt = pc + imm
                refs.setdefault(tgt, []).append((FLASH_BASE + pos, f"ldr.w r{rt}, [pc, #0x{imm:x}]"))
                pos += 4
                continue
            # 16-bit ADR: 1010 0 Rd(3) imm8
            if (hw & 0xF800) == 0xA000:
                rd = (hw >> 8) & 7
                imm = (hw & 0xFF) * 4
                pc = (FLASH_BASE + pos + 4) & ~3
                tgt = pc - imm  # ADR вычитает (forward ADR = subtract)
                refs.setdefault(tgt, []).append((FLASH_BASE + pos, f"adr r{rd}, 0x{tgt:08X}"))
            pos += 2
    return refs

app_regions = [(0x04000, 0x0F2E0)]
boot_regions = [(0x0204, 0x02800)]
refs = scan_literal_loads(donor, app_regions + boot_regions)

print("=== Ссылки PC-относительных загрузок на пул 0x0800E94A..0x0800E962 ===")
found = False
for tgt in range(0x0800E94A, 0x0800E964, 4):
    for a, s in refs.get(tgt, []):
        print(f"  цель 0x{tgt:08X} <- 0x{a:08X}: {s}")
        found = True
if not found:
    print("  (нет ссылок)")
print()

print("=== Все загрузки, чьи цели попадают в диапазон 0x0800E940..0x0800E970 ===")
found = False
for tgt in sorted(refs):
    if 0x0800E940 <= tgt <= 0x0800E970:
        for a, s in refs[tgt]:
            print(f"  цель 0x{tgt:08X} <- 0x{a:08X}: {s}")
            found = True
if not found:
    print("  (нет ссылок)")
print()

# ---------- 2. MOVW/MOVT пары, создающие 0x1FFFF7E8 или 0x080028E8 ----------
print("=== Поиск MOVW/MOVT пар для значений 0x1FFFF7E8 / 0x080028E8 (весь дамп) ===")
targets = {0x1FFFF7E8: [], 0x080028E8: []}
# сканируем всё приложение и бутлоадер
for (start_off, end_off) in app_regions + boot_regions:
    pos = start_off
    movw = {}  # reg -> (addr, imm16)
    while pos < end_off - 4:
        hw = struct.unpack_from("<H", data := donor, pos)[0] if False else struct.unpack_from("<H", donor, pos)[0]
        # MOVW: F240 0xxx
        if (hw & 0xFBF0) == 0xF240:
            hw2 = struct.unpack_from("<H", donor, pos+2)[0]
            imm16 = ((hw & 0xF) << 12) | ((hw2 & 0x7000) >> 4) | ((hw >> 10) & 0x300) >> ... if False else 0
        pos += 2
# (упрощённо: capstone-скан ниже сделает это надёжнее)
print("  -> см. capstone-скан ниже")
print()

# ---------- 3. Capstone: найти все инструкции, загружающие эти константы ----------
md = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_MCLASS)
md.detail = True
print("=== Capstone: инструкции с операндами-константами 0x1FFFF7E8/0x080028E8 или чтение [0x1FFFF7E8]/[0x080028E8] ===")
for (start_off, end_off) in app_regions + boot_regions:
    for ins in md.disasm(donor[start_off:end_off], FLASH_BASE + start_off):
        txt = f"{ins.mnemonic} {ins.op_str}"
        if "0x1ffff7e8" in txt.lower() or "0x80028e8" in txt.lower():
            print(f"  0x{ins.address:08X}: {txt}")
print()

# ---------- 4. Данные EEPROM донора по адресу 0x080028E8 ----------
print("=== Донор: данные EEPROM стр.1 (0x08002800..0x08002A00), слова 0x080028C0..0x08002900 ===")
for off in range(0x28C0, 0x2900, 16):
    row = donor[off:off+16]
    words = struct.unpack_from("<4I", donor, off)
    print(f"0x{FLASH_BASE+off:08X}: " + " ".join(f"{b:02X}" for b in row) + "   | " + " ".join(f"{w:08X}" for w in words))
