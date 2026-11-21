#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Дизассемблирование FUN_1000CD50 (сценарий подключения) sm2lib.dll 2.22.3.

Цель: понять, что происходит ПОСЛЕ команды 0x37 (LAUNCH) — какие команды
отправляются приложению и какой ответ приводит к ошибке
"Внутренняя ошибка микропрограммы %05lX" (код 00000).
"""
from capstone import *
import struct, sys

path = "/home/z/my-project/fw_analysis/new_dist/extracted/Scanmatik/sm2lib.dll"
d = open(path, "rb").read()
md = Cs(CS_ARCH_X86, CS_MODE_32)

# sm2lib.dll 2.22.3: ImageBase 0x10000000
# .text  VA 0x1000  VS 0x3E436  Raw 0x400
# .rdata VA 0x40000 VS 0x33C6E  Raw 0x3EA00
# .data  VA 0x74000 VS 0x83D0   Raw 0x72800
SECS = [
    (0x1000,  0x3E436, 0x400),
    (0x40000, 0x33C6E, 0x3EA00),
    (0x74000, 0x83D0,  0x72800),
    (0x7D000, 0x80,    0x78400),
]

def va2fo(va):
    rva = va - 0x10000000
    for vs, vsize, ro in SECS:
        if vs <= rva < vs + vsize:
            return ro + rva - vs
    return None

def fo2va(fo):
    for vs, vsize, ro in SECS:
        if ro <= fo < ro + vsize:
            return 0x10000000 + vs + (fo - ro)
    return None

def read_str_a(va, maxlen=60):
    fo = va2fo(va)
    if fo is None: return None
    s = d[fo:fo+maxlen].split(b'\x00')[0]
    try: return s.decode('cp1251')
    except: return None

def read_str_w(va, maxlen=60):
    fo = va2fo(va)
    if fo is None: return None
    raw = d[fo:fo+maxlen*2]
    txt = raw.split(b'\x00\x00')[0]
    try: return txt.decode('utf-16-le', errors='replace')
    except: return None

def disasm_func(start_va, max_len=0x1000, label=""):
    """Linear disassembly until ret + padding, with annotation of calls."""
    fo = va2fo(start_va)
    if fo is None:
        print(f"!! bad VA 0x{start_va:08X}")
        return
    code = d[fo:fo+max_len]
    print(f"\n===== {label} @ 0x{start_va:08X} =====")
    last_was_ret = False
    for ins in md.disasm(code, start_va):
        extra = ""
        # annotate immediate values that look like VAs
        if ins.mnemonic in ('call', 'jmp') and ins.op_str.startswith('0x'):
            tgt = int(ins.op_str, 16)
            s = read_str_a(tgt) or read_str_w(tgt)
            if s: extra = f"  ; \"{s[:40]}\""
        # annotate push imm / mov imm that look like rdata VAs (string ptrs)
        if ' ' in ins.op_str:
            parts = ins.op_str.split(', ')
            for p in parts:
                if p.startswith('0x'):
                    try: v = int(p, 16)
                    except: continue
                    if 0x10040000 <= v < 0x10074000:
                        s = read_str_w(v) or read_str_a(v)
                        if s and len(s) > 2:
                            extra += f"  ; -> \"{s[:50]}\""
                    elif 0x10074000 <= v < 0x1007C000:
                        extra += f"  ; .data"
        print(f"  0x{ins.address:08X}: {ins.bytes.hex():<22} {ins.mnemonic:<8} {ins.op_str}{extra}")
        # stop at ret followed by int3/nop padding
        if ins.mnemonic == 'ret':
            last_was_ret = True
        elif last_was_ret and ins.mnemonic in ('int3', 'nop'):
            break
        elif last_was_ret:
            break
        if ins.address > start_va + max_len:
            break

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "connect"
    if which == "connect":
        disasm_func(0x1000CD50, 0x600, "FUN_1000CD50 connection scenario")
    elif which.startswith("0x"):
        disasm_func(int(which, 16), 0x600, f"func @ {which}")
