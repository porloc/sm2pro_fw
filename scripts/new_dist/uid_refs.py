#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Поиск всех ссылок на 9 вхождений 0x1FFFF7E8 в новом приложении (LDR literal + ADR)."""
import struct

app = open("/home/z/my-project/fw_analysis/new_dist/dec_sm2_entry2.bin", "rb").read()
BASE = 0x08005000

UID_ADDRS = [0x0800C520, 0x0800D5C8, 0x0800D998, 0x0800DD7C, 0x0800E15C, 0x0800E700, 0x0800EACC, 0x0800EEA4, 0x0800F950]

def scan_literal_loads(data, start_off, end_off):
    refs = {}
    pos = start_off
    while pos < end_off - 1:
        hw = struct.unpack_from("<H", data, pos)[0]
        # 16-bit LDR literal: 0100 1 Rt imm8
        if (hw & 0xF800) == 0x4800:
            rt = (hw >> 8) & 7
            imm = (hw & 0xFF) * 4
            pc = (BASE + pos + 4) & ~3
            tgt = pc + imm
            refs.setdefault(tgt, []).append((BASE + pos, f"ldr r{rt}, [pc, #0x{imm:x}]"))
            pos += 2
            continue
        # 32-bit LDR.W literal
        if hw == 0xF8DF:
            hw2 = struct.unpack_from("<H", data, pos + 2)[0]
            rt = (hw2 >> 12) & 0xF
            imm = hw2 & 0xFFF
            pc = (BASE + pos + 4) & ~3
            tgt = pc + imm
            refs.setdefault(tgt, []).append((BASE + pos, f"ldr.w r{rt}, [pc, #0x{imm:x}]"))
            pos += 4
            continue
        pos += 2
    return refs

refs = scan_literal_loads(app, 0, len(app))
print("=== Ссылки на вхождения 0x1FFFF7E8 ===")
for ua in UID_ADDRS:
    rr = refs.get(ua, [])
    print(f"0x{ua:08X}: " + ("; ".join(f"0x{a:08X} ({s})" for a, s in rr) if rr else "(прямых LDR-ссылок нет)"))
print()

# Также: значения слов вокруг каждого вхождения (пул литералов)
print("=== Контекст пулов (по 4 слова вокруг) ===")
for ua in UID_ADDRS:
    off = ua - BASE
    words = struct.unpack_from("<8I", app, off - 16)
    print(f"0x{ua:08X}: " + " ".join(f"{w:08X}" for w in words))
