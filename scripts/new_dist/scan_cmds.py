#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Сканирование sm2lib.dll 2.22.3: где какие команды протокола отправляются.

Паттерн: mov byte ptr [reg + 0x24], imm8   (C6 40..47 24 XX)
Также:   mov byte ptr [reg + 0x24], reg8   (88 40..47 24)
Выводим карту команда -> адреса -> функции.
"""
from capstone import *
import struct, re

DLL = "/home/z/my-project/fw_analysis/new_dist/extracted/Scanmatik/sm2lib.dll"
d = open(DLL, "rb").read()
md = Cs(CS_ARCH_X86, CS_MODE_32)

# .text VA 0x1000, raw 0x400, size 0x3E436
TEXT_VA = 0x10000000 + 0x1000
TEXT_RAW = 0x400
TEXT_SZ = 0x3E436

# find all C6 4x 24 xx (mov byte [reg+0x24], imm8)
hits = {}
for i in range(TEXT_RAW, TEXT_RAW + TEXT_SZ - 4):
    if d[i] == 0xC6 and 0x40 <= d[i+1] <= 0x47 and d[i+2] == 0x24:
        imm = d[i+3]
        va = TEXT_VA + (i - TEXT_RAW)
        hits.setdefault(imm, []).append(va)

print("Команды, отправляемые из sm2lib.dll (mov byte [r+0x24], imm):")
for imm in sorted(hits):
    print(f"  cmd 0x{imm:02X}: {[hex(v) for v in hits[imm]]}")

# Определим границы функций: сканируем назад от каждого хита до последовательности
# CC CC (int3 padding) или до push ebp; проще: дизассемблируем окно и ищем ближайший
# предшествующий 'push ebp; mov ebp, esp' (55 8B EC)
def find_func_start(va):
    fo = TEXT_RAW + (va - TEXT_VA)
    for back in range(fo, max(TEXT_RAW, fo - 0x3000), -1):
        if d[back-1] == 0xCC and d[back] != 0xCC:
            # начало функции после int3 паддинга
            return TEXT_VA + (back - TEXT_RAW)
    return None

print("\nКоманда -> функция:")
for imm in sorted(hits):
    funcs = sorted(set(find_func_start(v) or 0 for v in hits[imm]))
    print(f"  cmd 0x{imm:02X}: funcs {[hex(f) for f in funcs]}")
