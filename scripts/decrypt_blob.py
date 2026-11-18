#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Дешифровка блоба прошивки из sm2lib.dll поточным шифром бутлоадера SM2."""
import struct

M32 = 0xFFFFFFFF

def ror(x, n):
    n &= 31
    if n == 0: return x & M32
    return ((x >> n) | (x << (32 - n))) & M32

def decrypt_blob(blob, seed, A=0xCAFE1381, K1=0x13AB3377, K2=0x5188016B):
    """Обратное преобразование FUN_08000fb0: dec = ROR(((((w-A)^K1)+2B)^B)-8B,17); B+=A*8;B^=B>>1;A=(ROR(w,7)^A)+K2"""
    out = bytearray(len(blob))
    a, b = A, seed
    for i in range(0, len(blob), 4):
        w = struct.unpack_from("<I", blob, i)[0]
        t = ((((w - a) & M32) ^ K1) + 2 * b & M32) & M32
        t = (t ^ b) & M32
        t = (t - 8 * b) & M32
        dec = ror(t, 17)
        struct.pack_into("<I", out, i, dec)
        b = (b + a * 8) & M32
        b = (b ^ (b >> 1)) & M32
        a = (ror(w, 7) + 0)  # placeholder
        a = (ror(w, 7) ^ a if False else (ror(w, 7) ^ A))
        # Внимание: A обновляется через СТАРОЕ A
        a = (ror(w, 7) ^ A) & M32
        a = (a + K2) & M32
        A = a
    return bytes(out)

# === Извлечение блоба из sm2lib.dll ===
DLL = "/home/z/my-project/fw_analysis/driver/Scanmatik/sm2lib.dll"
d = open(DLL, "rb").read()

blobs = [
    ("Type 1/2/3 (SM2 STM32F105)", 0x40080, 0xB2E0, 0x7821AB35),
    ("Type 5", 0x4C3C8, 0xF474, 0x3F60B252),
]

# === Наш дамп для сравнения ===
BIN = "/home/z/my-project/fw_analysis/SM2_2.21.32_A111788_STM32F105VCT6.bin"
ref = open(BIN, "rb").read()
ref_app = ref[0x4000:0x4000+0xB800]

for name, off, size, seed in blobs:
    blob = d[off:off+size]
    dec = decrypt_blob(blob, seed)
    sp, rst = struct.unpack_from("<II", dec, 0)
    print(f"=== {name}: blob@0x{off:X} size=0x{size:X} seed=0x{seed:08X} ===")
    print(f"  Расшифровано: SP=0x{sp:08X}, Reset=0x{rst:08X}")
    # Сравнение с референсным дампом
    match = sum(1 for i in range(0, min(len(dec), 0x200), 4)
                if struct.unpack_from('<I', dec, i)[0] == struct.unpack_from('<I', ref_app, i)[0])
    print(f"  Совпадение слов с референсом (первые 512Б): {match}/{0x200//4}")
    fn = f"/home/z/my-project/fw_analysis/decrypted_{name.split()[0].replace('/','_')}.bin"
    open(fn, "wb").write(dec)
    print(f"  Сохранено: {fn}")
    print()
