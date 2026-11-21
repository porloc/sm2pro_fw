#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Сборка v6: образ 2.22.3 patched_v2 + патч SWD_KEEP (SWD жив после LAUNCH).

НАЙДЕНО (реверс, scripts/scan_debug_block2.py; docs/JLINK_OB_GUIDE.md, 3а):
донорский бутлоадер 2.21.32 (и 2.21.35) при запуске приложения (команда 0x37
LAUNCH, блок 0x0800132A, вызов bl 0x08000E14 на 0x0800133C) ОТКЛЮЧАЕТ SWD:

  0x08000E14: ldr   r0, [pc, #0x330]   ; r0 = 0x40010000 (AFIO)
  0x08000E16: ldr   r1, [r0, #4]       ; AFIO_MAPR
  0x08000E18: bic   r1, r1, #0x07000000
  0x08000E1C: orr   r1, r1, #0x04000000 ; SWJ_CFG = 100: JTAG+SWD ВЫКЛ
  0x08000E20: str   r1, [r0, #4]

Единственный вызов функции — из блока LAUNCH; в простое бутлоадера SWD жив.
Поэтому живое подключение к работающему/зависшему приложению всегда падает
("Failed to initialize DAP" / "Could not read memory" / "CPU is not halted") —
так было и в логах дампов A/B, и во всех последующих попытках.

Патч v6 (4 байта @0x0800E1C):
  41 F0 80 61  orr.w r1, r1, #0x04000000   (SWJ_CFG=100, SWD выкл)
               ->
  41 F0 00 71  orr.w r1, r1, #0x02000000   (SWJ_CFG=010: JTAG выкл, SWD ВКЛ)

Итог: бутлоадер больше не убивает SWD при запуске приложения — возможны
брейкпоинты/останов/чтение RAM у ЗАПУЩЕННОГО приложения 2.22.3 (бонус-прогон:
вход в крипто-ядро 0x0800C15C, возврат 0x08007292).

База: patched_v2 (MD5 d0a3aadf125b8ff190ad62ced4650dcc)
Выход: SM2Pro_full_flash_2.22.3_patched_v2_SWDON.bin
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# Где искать базовый образ patched_v2: рядом, в дереве репозитория, на исходном стенде
CANDIDATES = [
    os.path.join(HERE, "SM2Pro_full_flash_2.22.3_patched_v2.bin"),
    os.path.join(HERE, "..", "..", "firmware", "SM2Pro_full_flash_2.22.3_patched_v2.bin"),
    "/home/z/my-project/fw_analysis/OUTPUT/SM2Pro_full_flash_2.22.3_patched_v2.bin",
]

OFF = 0xE1C                      # оффсет команды orr в AFIO_MAPR-блоке (0x08000E1C)
OLD = bytes.fromhex("41f08061")  # orr.w r1, r1, #0x04000000 (SWJ_CFG=100)
NEW = bytes.fromhex("41f00071")  # orr.w r1, r1, #0x02000000 (SWJ_CFG=010, SWD жив)
EXPECTED_CTX = bytes.fromhex("cc48416821f0e06141f080614160")  # 0x08000E14..E21

# Эталон собранного образа (см. README, раздел «Хэши образов»)
EXPECTED_MD5 = "25d162dcb8f4ae74c85ae2ac339d69f4"
EXPECTED_SHA256 = "41d4ec2fae620b37feeacca13737fa06fa2ec3e5c0093efbba554c73dbd2285c"

base = None
for c in CANDIDATES:
    if os.path.isfile(c):
        base = c
        break
if base is None:
    print("Не найден базовый образ patched_v2:", CANDIDATES)
    sys.exit(1)

img = bytearray(open(base, "rb").read())
ctx = bytes(img[0xE14:0xE22])
if ctx != EXPECTED_CTX:
    print("ОШИБКА: неожиданные байты базы @0xE14:", ctx.hex())
    print("ожидалось:", EXPECTED_CTX.hex())
    sys.exit(1)

img[OFF:OFF + 4] = NEW

outs = []
for out in (os.path.join(HERE, "SM2Pro_full_flash_2.22.3_patched_v2_SWDON.bin"),
            os.path.normpath(os.path.join(HERE, "..", "..", "firmware",
                                          "SM2Pro_full_flash_2.22.3_patched_v2_SWDON.bin"))):
    try:
        open(out, "wb").write(bytes(img))
        outs.append(out)
    except OSError:
        pass

d = bytes(img)
md5 = hashlib.md5(d).hexdigest()
sha = hashlib.sha256(d).hexdigest()
print(f"OK: база {base}")
for out in outs:
    print(f"    записан {out}")
print(f"  MD5      : {md5}")
print(f"  SHA256   : {sha}")
print(f"  патч     : @0x0800E1C {OLD.hex()} -> {NEW.hex()}")
print("             (SWJ_CFG 100 -> 010: JTAG выкл, SWD остаётся ВКЛЮЧЁН после LAUNCH)")
if md5 != EXPECTED_MD5 or sha != EXPECTED_SHA256:
    print("ВНИМАНИЕ: хэш не совпал с эталоном!")
    sys.exit(2)
print("Хэши совпали с эталоном.")

# контрольная дизассемблерная проверка
try:
    from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    print("\nпроверка (дизассемблер):")
    for ins in md.disasm(d[0xE14:0xE22], 0x08000E14):
        print(f"  0x{ins.address:08X}: {ins.bytes.hex():10s} {ins.mnemonic} {ins.op_str}")
except ImportError:
    print("(capstone недоступен — дизассемблерная проверка пропущена)")
