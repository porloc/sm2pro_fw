#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Дизассемблировать функцию, содержащую 0x0800E7CC (ldr r0 -> 0x0800E958)."""
from capstone import *
import struct

DIR = "/home/z/my-project/fw_analysis/"
donor = open(DIR + "SM2_2.21.32_A111788_STM32F105VCT6.bin", "rb").read()
FLASH_BASE = 0x08000000
md = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_MCLASS)
md.detail = True

# Пул литералов: 0x0800E94C..0x0800E964. Ищем начало функции: PUSH с LR перед 0x0800E790.
pool = {
    0x0800E94C: struct.unpack_from("<I", donor, 0x0E94C)[0],
    0x0800E950: struct.unpack_from("<I", donor, 0x0E950)[0],
    0x0800E954: struct.unpack_from("<I", donor, 0x0E954)[0],
    0x0800E958: struct.unpack_from("<I", donor, 0x0E958)[0],
    0x0800E95C: struct.unpack_from("<I", donor, 0x0E95C)[0],
    0x0800E960: struct.unpack_from("<I", donor, 0x0E960)[0],
    0x0800E964: struct.unpack_from("<I", donor, 0x0E964)[0],
}
print("Пул литералов функции:")
for a, v in pool.items():
    print(f"  0x{a:08X}: 0x{v:08X}")
print()

start = 0x0E728  # кандидат: PUSH с LR
print(f"=== Функция с 0x{FLASH_BASE+start:08X} до 0x0800E8B2 ===")
for ins in md.disasm(donor[start:0x0E8B2], FLASH_BASE + start):
    extra = ""
    # Аннотируем LDR [pc] попадания в пул
    if ins.mnemonic.startswith("ldr") and "[pc" in ins.op_str:
        # вычислим цель
        import re
        m = re.search(r"\[pc, #(0x[0-9a-f]+)\]", ins.op_str)
        if m:
            imm = int(m.group(1), 16)
            pc = (ins.address + 4) & ~3
            tgt = pc + imm
            if tgt in pool:
                extra = f"   ; 0x{tgt:08X} = 0x{pool[tgt]:08X}"
    if ins.mnemonic == "bl" or ins.mnemonic.startswith("b"):
        pass
    print(f"  0x{ins.address:08X}: {ins.bytes.hex():<12} {ins.mnemonic:<9} {ins.op_str}{extra}")
