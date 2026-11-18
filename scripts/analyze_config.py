#!/usr/bin/env python3
"""Hexdump области конфига + поиск серийника."""
import struct

BIN = "/home/z/my-project/fw_analysis/SM2_2.21.32_A111788_STM32F105VCT6.bin"
data = open(BIN, "rb").read()

def hexdump(off, length):
    for i in range(0, length, 16):
        chunk = data[off+i:off+i+16]
        if len(chunk) == 0: break
        hexs = " ".join(f"{b:02X}" for b in chunk)
        asc = "".join(chr(b) if 0x20 <= b < 0x7f else "." for b in chunk)
        print(f"  0x{off+i:06X} | {hexs:<47} | {asc}")

print("=== Область 0xF000-0xF800 (конфиг/серийники) ===")
hexdump(0xF000, 0x800)

print()
print("=== Поиск 'A111788' и похожих ===")
import re
for pat in [b"A111788", b"111788", b"788"]:
    idxs = [m.start() for m in re.finditer(re.escape(pat), data)]
    print(f"  {pat!r}: {idxs}")

print()
print("=== Конец блока бутлоадера (0x2F80-0x3000), маркер A55A ===")
hexdump(0x2FC0, 0x40)
