#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Финальная дешифровка обоих блобов + полное сравнение с референсом."""
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

DLL = "/home/z/my-project/fw_analysis/driver/Scanmatik/sm2lib.dll"
d = open(DLL, "rb").read()
ref = open("/home/z/my-project/fw_analysis/SM2_2.21.32_A111788_STM32F105VCT6.bin", "rb").read()

# Type 1/2/3: SM2 STM32F105 — file 0x40080, size 0xB2E0, seed 0x7821AB35
blob1 = d[0x40080:0x40080+0xB2E0]
dec1 = decrypt_blob(blob1, 0x7821AB35)
open("/home/z/my-project/fw_analysis/app_sm2_2.21.32_decrypted.bin", "wb").write(dec1)

ref_app = ref[0x4000:0x4000+0xB2E0]
same = sum(1 for i in range(0, len(dec1), 4) if dec1[i:i+4] == ref_app[i:i+4])
total = len(dec1)//4
print(f"Type1/2/3 (SM2 app 2.21.32): {same}/{total} слов совпало ({100*same/total:.3f}%)")
diffs = [i for i in range(0, len(dec1), 4) if dec1[i:i+4] != ref_app[i:i+4]]
print(f"  Различающихся слов: {len(diffs)}")
for i in diffs[:10]:
    print(f"    flash 0x{0x08004000+i:08X}: dll={dec1[i:i+4].hex()} bin={ref_app[i:i+4].hex()}")

# Type 5: пробуем разные параметры
print()
print("Type 5 blob: пробуем вариации ключей/seed...")
blob5 = d[0x4C3C8:0x4C3C8+0xF474]
for seed in [0x3F60B252, 0x43719874]:
    for k1c, k2c in [(0x13AB3377, 0x5188016B)]:
        dec = decrypt_blob(blob5, seed, 0xCAFE1381, k1c, k2c)
        sp, rst = struct.unpack_from("<II", dec, 0)
        valid = 0x20000000 <= sp <= 0x20020000 and 0x08000001 <= rst <= 0x08040001 and rst & 1
        print(f"  seed=0x{seed:08X}: SP=0x{sp:08X} Reset=0x{rst:08X} {'<<< ВАЛИДНО!' if valid else ''}")
