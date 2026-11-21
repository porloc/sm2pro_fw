#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Дизассемблирование приложения 2.22.3 (base 0x08005000): диспетчер и обработчики.

Цель: понять, какие команды обслуживает приложение и что оно отвечает,
найти обработчик 0x86 (эхо) и команды, возвращающие код ошибки.
"""
from capstone import *
import struct, sys

APP = "/home/z/my-project/fw_analysis/new_dist/dec_sm2_entry2.bin"
data = open(APP, "rb").read()
BASE = 0x08005000
md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
md.detail = False

def dis(addr, size, title=""):
    off = addr - BASE
    if off < 0 or off >= len(data):
        print(f"!! 0x{addr:08X} вне диапазона")
        return
    print(f"--- {title} @ 0x{addr:08X} ---")
    for ins in md.disasm(data[off:off+size], addr):
        extra = ""
        # аннотируем литералы-указатели в пределах приложения
        if ins.mnemonic.startswith('ldr') and '[pc' in ins.op_str:
            try:
                # вычисляем адрес литерала
                idx = ins.op_str.index('#')
                imm = int(ins.op_str[idx+1:].rstrip(']'), 0)
                lit_addr = (ins.address + 4 + imm) & ~3
                loff = lit_addr - BASE
                if 0 <= loff <= len(data)-4:
                    w = struct.unpack_from('<I', data, loff)[0]
                    if BASE <= w < BASE+len(data):
                        extra = f"   ; =0x{w:08X} (в приложении)"
                    elif 0x08000000 <= w < 0x08040000:
                        extra = f"   ; =0x{w:08X} (флеш)"
                    elif 0x1FFFF000 <= w < 0x20000000:
                        extra = f"   ; =0x{w:08X} (система)"
            except Exception:
                pass
        print(f"  0x{ins.address:08X}: {ins.bytes.hex():<12} {ins.mnemonic:<10} {ins.op_str}{extra}")
    print()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].startswith('0x'):
        a = int(sys.argv[1], 16)
        n = int(sys.argv[2], 0) if len(sys.argv) > 2 else 0x80
        dis(a, n, "запрошено")
    else:
        dis(0x0800C2CA - 0x60, 0x140, "диспетчер 0x0800C2CA (контекст)")
