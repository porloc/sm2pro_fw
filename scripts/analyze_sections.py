#!/usr/bin/env python3
"""Детальный осмотр границ секций и данных."""
import struct, re

BIN = "/home/z/my-project/fw_analysis/SM2_2.21.32_A111788_STM32F105VCT6.bin"
FLASH_BASE = 0x08000000
data = open(BIN, "rb").read()

def hexdump(off, length, title=""):
    print(f"=== {title} (offset 0x{off:X}, flash 0x{FLASH_BASE+off:08X}) ===")
    for i in range(0, length, 16):
        chunk = data[off+i:off+i+16]
        if len(chunk) == 0: break
        hexs = " ".join(f"{b:02X}" for b in chunk)
        asc = "".join(chr(b) if 0x20 <= b < 0x7f else "." for b in chunk)
        print(f"  0x{off+i:06X} | {hexs:<47} | {asc}")
    print()

# Границы: конец первого блока (0x2FFF), зазор, начало второго (0x4000)
hexdump(0x2F00, 0x100, "Конец первого блока (перед зазором)")
hexdump(0x4000, 0x100, "Начало второго блока 0x08004000")
hexdump(0x3F80, 0x80, "Перед 0x08004000 (конец зазора)")

# Поиск валидных Thumb-указателей в начале 0x4000
print("Слова по offset 0x4000:")
for i in range(16):
    v = struct.unpack_from("<I", data, 0x4000 + i*4)[0]
    print(f"  [0x4000+{i*4:#04x}] = 0x{v:08X}")

# Все строки во всём дампе
print()
print("=== Все ASCII строки (>=6 симв) во всём дампе ===")
for m in re.finditer(rb"[\x20-\x7e]{6,}", data):
    s = m.group().decode('ascii')
    if not re.match(r'^[@`\x27\x2c\x3b\xa0]*$', s):
        print(f"  0x{m.start():06X}: {s!r}")

# Юникод (UTF-16LE) строки — часто в STM32 для USB дескрипторов
print()
print("=== UTF-16LE строки (>=6 симв) ===")
for m in re.finditer(rb"(?:[\x20-\x7e]\x00){6,}", data):
    print(f"  0x{m.start():06X}: {m.group().decode('utf-16-le')!r}")
