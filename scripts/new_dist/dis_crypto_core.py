#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Дизассемблер крипто-ядра 0x0800C15C приложения 2.22.3.

Цель: понять, почему ядро зависает на донорском бутлоадере 2.21.32.
Ищем: вызовы svc (номера сервисов), обращения к периферии
(0x40000000-0x40030000, 0xE0000000+), циклы (обратные ветвления),
чтение UID-пула 0x0800C520.
"""
import sys

from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB

BASE = 0x08000000
IMG = "/home/z/my-project/fw_analysis/OUTPUT/SM2Pro_full_flash_2.22.3_patched_v2.bin"

md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
md.detail = False


def disasm(start_va, length, img, label=""):
    print(f"===== {label or hex(start_va)}: 0x{start_va:08X}..0x{start_va+length:08X}")
    code = img[start_va - BASE:start_va - BASE + length]
    for ins in md.disasm(code, start_va):
        extra = ""
        op = ins.op_str
        # аннотации
        for tok in op.replace(",", " ").split():
            tok = tok.strip("[]!#")
            if tok.startswith("0x") or tok.startswith("#0x"):
                try:
                    v = int(tok.lstrip("#"), 16)
                except ValueError:
                    continue
                if 0x40000000 <= v < 0x40030000:
                    extra += f"  ; ПЕРИФЕРИЯ 0x{v:08X}"
                elif v >= 0xE0000000:
                    extra += f"  ; SystemControl 0x{v:08X}"
                elif 0x0800C500 <= v <= 0x0800C540:
                    extra += f"  ; UID-пул auth"
                elif v == 0x1FFFF7E8:
                    extra += "  ; HW UID!"
                elif v == 0x080028E8:
                    extra += "  ; виртуальный UID (EEPROM)"
                elif 0x08002800 <= v < 0x08003000:
                    extra += f"  ; EEPROM 0x{v:08X}"
        if ins.mnemonic == "svc":
            extra += "  ; <<< СЕРВИС БУТЛОАДЕРА"
        print(f"  0x{ins.address:08X}:  {ins.bytes.hex():12s} {ins.mnemonic:8s} {ins.op_str}{extra}")


def find_back_branches(start_va, length, img):
    """Найти обратные ветвления (циклы) в диапазоне."""
    code = img[start_va - BASE:start_va - BASE + length]
    loops = []
    for ins in md.disasm(code, start_va):
        if ins.mnemonic.startswith("b") and not ins.mnemonic.startswith("bl"):
            try:
                target = int(ins.op_str.replace("#", ""), 16)
            except ValueError:
                continue
            if target < ins.address:
                loops.append((ins.address, target))
    return loops


if __name__ == "__main__":
    img = open(IMG, "rb").read()
    start = 0x0800C15C
    length = int(sys.argv[1], 0) if len(sys.argv) > 1 else 0x300
    disasm(start, length, img, "крипто-ядро AUTH")
    print("\n===== Обратные ветвления (циклы):")
    for a, t in find_back_branches(start, length, img):
        print(f"  0x{a:08X} -> 0x{t:08X}  (размер цикла {a - t} Б)")
