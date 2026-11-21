#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Дешифровка блобов прошивки из нового sm2lib.dll (2.22.3) — запись параметров из функции 0x1000C760."""
import struct

M32 = 0xFFFFFFFF

def ror(x, n):
    n &= 31
    if n == 0: return x & M32
    return ((x >> n) | (x << (32 - n))) & M32

def decrypt_blob(blob, seed, A=0xCAFE1381, K1=0x13AB3377, K2=0x5188016B):
    out = bytearray(len(blob))
    a, b = A, seed
    for i in range(0, len(blob), 4):
        w = struct.unpack_from("<I", blob, i)[0]
        t = (((((w - a) & M32) ^ K1) + 2 * b) & M32) ^ b
        t = (t - 8 * b) & M32
        dec = ror(t, 17)
        struct.pack_into("<I", out, i, dec)
        b = (b + a * 8) & M32
        b = (b ^ (b >> 1)) & M32
        a = ((ror(w, 7) ^ a) + K2) & M32
    return bytes(out)

def stm32_crc(data):
    def rev32(x):
        return int("{:032b}".format(x)[::-1], 2)
    crc = 0xFFFFFFFF
    for i in range(0, len(data), 4):
        w = rev32(struct.unpack_from("<I", data, i)[0])
        crc ^= w
        for _ in range(32):
            crc = ((crc << 1) ^ 0x04C11DB7) & M32 if crc & 0x80000000 else (crc << 1) & M32
    return rev32(crc) ^ 0xFFFFFFFF

DLL = "/home/z/my-project/fw_analysis/new_dist/extracted/Scanmatik/sm2lib.dll"
d = open(DLL, "rb").read()

# Из функции 0x1000C760 (SM2 = типы 1/2/3), два вхождения по 0x1C:
#   entry1: seed=0x7821AB35, ver=0x1198, size=0xB00,  crc=0x2912D0A0, ptrs 0x100594F8/0x10059FF8/0x1005A018
#   entry2: seed=0x7821AB35, ver=0x1198, size=0x1353C, crc=0x210E9A13, ptrs 0x10045FB8/0x10045F98/0x10045F50
# VA->file: file = 0x3EA00 + (VA - 0x10040000)
def va2f(va): return 0x3EA00 + (va - 0x10040000)

entries = [
    ("SM2 entry1 (0xB00)",   0x100594F8, 0xB00,   0x7821AB35, 0x2912D0A0, [0x100594F8, 0x10059FF8, 0x1005A018]),
    ("SM2 entry2 (0x1353C)", 0x10045F50, 0x1353C, 0x7821AB35, 0x210E9A13, [0x10045FB8, 0x10045F98, 0x10045F50]),
    ("Type5 (0xF2CC)",       0x1005A060, 0xF2CC,  0x43719874, 0x83BBF98A, [0x1005A060, 0x1006932C, 0x10069350]),
]

for name, ptr1, size, seed, crc_expect, ptrs in entries:
    off = va2f(ptr1)
    blob = d[off:off+size]
    dec = decrypt_blob(blob, seed)
    sp, rst = struct.unpack_from("<II", dec, 0)
    crc = stm32_crc(dec)
    print(f"=== {name}: file 0x{off:X}, size 0x{size:X}, seed 0x{seed:08X} ===")
    print(f"  SP=0x{sp:08X} Reset=0x{rst:08X}")
    print(f"  CRC32(STM32) = 0x{crc:08X} (ожидается 0x{crc_expect:08X}) {'СОВПАЛ!' if crc == crc_expect else 'нет'}")
    valid_vec = 0x20000000 <= sp <= 0x20020000 and (sp & 7) == 0 and 0x08000001 <= rst <= 0x08040001 and (rst & 1) == 1
    print(f"  Валидные векторы: {'ДА' if valid_vec else 'НЕТ'}")
    print(f"  Первые 32 байта: {dec[:32].hex()}")
    fn = "/home/z/my-project/fw_analysis/new_dist/dec_" + name.split()[0].lower() + ("_a.bin" if "entry1" in name else "_b.bin" if "entry2" in name else "_t5.bin")
    open(fn, "wb").write(dec)
    print(f"  Сохранено: {fn}")
    print()
