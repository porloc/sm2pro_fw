#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Дизассемблирование PC-кода (smj2534.dll, smwin.exe) вокруг 0x3EA816AB."""
from capstone import *
import struct

md = Cs(CS_ARCH_X86, CS_MODE_32)

def parse_sections(data):
    e_lfanew = struct.unpack_from('<I', data, 0x3C)[0]
    opt_size = struct.unpack_from('<H', data, e_lfanew + 20)[0]
    num_sec = struct.unpack_from('<H', data, e_lfanew + 6)[0]
    base = struct.unpack_from('<I', data, e_lfanew + 52 + 28)[0]  # ImageBase
    secs = []
    sec_off = e_lfanew + 24 + opt_size
    for i in range(num_sec):
        o = sec_off + i * 40
        name = data[o:o+8].rstrip(b'\x00').decode('ascii', 'ignore')
        vsize, vaddr, rsize, raddr = struct.unpack_from('<IIII', data, o + 8)
        secs.append((name, vaddr, vsize, raddr, rsize))
    return base, secs

def file_to_va(off, base, secs):
    for name, vaddr, vsize, raddr, rsize in secs:
        if raddr <= off < raddr + rsize:
            return base + vaddr + (off - raddr), name
    return None, None

for f, hit in [("smj2534.dll", 0x30BB45), ("smwin.exe", 0x2C2710)]:
    data = open(f, "rb").read()
    base, secs = parse_sections(data)
    va, sec = file_to_va(hit, base, secs)
    print(f"=== {f}: hit file:0x{hit:X} -> VA 0x{va:08X} (секция {sec}, ImageBase 0x{base:X}) ===")
    # Дизассемблируем окно вокруг (ищем назад выровненный старт — просто от hit-0x200)
    start = hit - 0x180
    code = data[start:hit + 0x100]
    va_start = file_to_va(start, base, secs)[0]
    for ins in md.disasm(code, va_start):
        mark = "   <<<< 0x3EA816AB" if ins.address <= va < ins.address + ins.size else ""
        print(f"  0x{ins.address:08X}: {ins.bytes.hex():<20} {ins.mnemonic:<8} {ins.op_str}{mark}")
    print()
