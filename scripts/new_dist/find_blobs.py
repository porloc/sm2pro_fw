#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Поиск ссылок на зашифрованные блобы в новом sm2lib.dll (2.22.3) и извлечение параметров обновления."""
from capstone import *
import struct, pefile

DLL = "/home/z/my-project/fw_analysis/new_dist/extracted/Scanmatik/sm2lib.dll"
d = open(DLL, "rb").read()

pe = pefile.PE(DLL, fast_load=True)
IMAGE_BASE = pe.OPTIONAL_HEADER.ImageBase
secs = [(s.Name.decode().rstrip(chr(0)), s.VirtualAddress, s.Misc_VirtualSize, s.PointerToRawData, s.SizeOfRawData) for s in pe.sections]
print("Sections:", [(n, hex(va), hex(vs), hex(r), hex(rs)) for n, va, vs, r, rs in secs])

def file_to_va(off):
    for n, va, vs, r, rs in secs:
        if r <= off < r + rs:
            return IMAGE_BASE + va + (off - r), n
    return None, None

def va_to_file(vaddr):
    for n, va, vs, r, rs in secs:
        if va <= (vaddr - IMAGE_BASE) < va + vs:
            return r + (vaddr - IMAGE_BASE - va), n
    return None, None

# High-entropy region 0x45000-0x68000 -> VA range
lo_va = file_to_va(0x45000)[0]
hi_va = file_to_va(0x68000)[0]
print(f"Blob VA range: 0x{lo_va:08X}..0x{hi_va:08X}")

# Scan .text for 'mov reg, imm32' (B8..BF) with imm in blob VA range
text_name, text_va, text_vs, text_raw, text_rs = secs[0]
hits = []
for i in range(text_raw, text_raw + text_rs - 5):
    op = d[i]
    if 0xB8 <= op <= 0xBF:
        imm = struct.unpack_from("<I", d, i + 1)[0]
        if lo_va <= imm < hi_va:
            reg = ["eax","ecx","edx","ebx","esp","ebp","esi","edi"][op - 0xB8]
            hits.append((i, reg, imm))

print(f"\nНайдено ссылок на блоб-регион: {len(hits)}")
for off, reg, imm in hits:
    va, sec = file_to_va(off)
    print(f"  file 0x{off:X} VA 0x{va:08X}: mov {reg}, 0x{imm:08X}  (blob file 0x{va_to_file(imm)[0]:X})")

# Disassemble window around each hit
md = Cs(CS_ARCH_X86, CS_MODE_32)
print("\n" + "=" * 70)
for off, reg, imm in hits:
    va, _ = file_to_va(off)
    start = max(text_raw, off - 0x40)
    va_start, _ = file_to_va(start)
    print(f"\n--- Контекст вокруг file 0x{off:X} (VA 0x{va:08X}) ---")
    for ins in md.disasm(d[start:off + 0x60], va_start):
        mark = " <<<< BLOB REF" if ins.address == va else ""
        print(f"  0x{ins.address:08X}: {ins.bytes.hex():<16} {ins.mnemonic:<7} {ins.op_str}{mark}")
