#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Разведка DLL: экспорты, импорты, строки, поиск образов прошивки."""
import pefile, sys, re, os

DRIVER = "/home/z/my-project/fw_analysis/driver/Scanmatik"

def analyze(path):
    print(f"\n{'='*70}\n=== {os.path.basename(path)} ({os.path.getsize(path)} байт)\n{'='*70}")
    pe = pefile.PE(path, fast_load=True)
    pe.parse_data_directories(directories=[
        pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IMPORT'],
        pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_EXPORT']])
    # Архитектура
    m = pe.FILE_HEADER.Machine
    print(f"Machine: {'x86' if m==0x14c else 'x64' if m==0x8664 else hex(m)}")
    # Экспорты
    try:
        if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
            exps = [e.name.decode() if e.name else f"#{e.ordinal}" for e in pe.DIRECTORY_ENTRY_EXPORT.symbols]
            print(f"Exports ({len(exps)}): {', '.join(exps[:40])}{' ...' if len(exps)>40 else ''}")
    except Exception as e:
        print(f"Exports: err {e}")
    # Импорты
    try:
        if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
            for d in pe.DIRECTORY_ENTRY_IMPORT:
                names = [i.name.decode() for i in d.imports if i.name][:8]
                print(f"  Import {d.dll.decode()}: {len(d.imports)} funcs ({', '.join(names)}...)")
    except Exception as e:
        pass
    # Секции
    for s in pe.sections:
        print(f"  Section {s.Name.decode().rstrip(chr(0))}: VA=0x{s.VirtualAddress:08X} VSize=0x{s.Misc_VirtualSize:08X} RawSize=0x{s.SizeOfRawData:08X} Char=0x{s.Characteristics:08X}")
    pe.close()

for f in ["sm2lib.dll", "smj2534.dll", "china.dll", "plxlib.dll"]:
    analyze(os.path.join(DRIVER, f))
