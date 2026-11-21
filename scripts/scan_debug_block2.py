#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Точная проверка: закрывает ли прошивка SM2 Pro отладку (SWD)?

Проверяем по образам (бутлоадер 0x08000000-0x08001197 + приложение):
  1. AFIO_MAPR 0x40010004: есть ли литерал в пуле, кто его грузит,
     пишутся ли биты SWJ_CFG (0x02000000 JTAG-off / 0x04000000 SWD-off).
  2. FLASH_OPTKEYR 0x40022008 / KEYR 0x40022004 / OBR 0x4002201C /
     option bytes 0x1FFFF800 — программирование защиты (RDP) на ходу.
  3. DBGMCU_CR 0xE0042004, PWR 0x40007000, SCB SCR 0xE000ED10 — сон.
  4. FPB 0xE0002000-0xE0002024, DEMCR 0xE000EDFC, DHCSR 0xE000EDF0 —
     самомодификация отладки.
  5. WFI (0xBF30) / WFE (0xBF20) — режимы сна (без DBG_SLEEP отладка мертва).
Вывод: только точные находки с чистым контекстом от самой команды.
"""
import struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB

BASE = 0x08000000
md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
md.detail = False

IMAGES = [
    ("донор 2.21.32 (бут всех v2-образов)",
     "/home/z/my-project/fw_analysis/OUTPUT/SM2Pro_full_flash_2.21.32_donor_asis.bin"),
    ("рабочая 2.21.35",
     "/home/z/my-project/fw_analysis/v2_21_35/fw_22135.bin"),
    ("patched_v2 2.22.3",
     "/home/z/my-project/fw_analysis/OUTPUT/SM2Pro_full_flash_2.22.3_patched_v2.bin"),
]

WATCH = {
    0x40010004: "AFIO_MAPR — SWJ_CFG!",
    0x40010000: "AFIO_EVCR",
    0x40022004: "FLASH_KEYR",
    0x40022008: "FLASH_OPTKEYR — RDP!",
    0x40022010: "FLASH_CR",
    0x4002201C: "FLASH_OBR",
    0x40022020: "FLASH_WRPR",
    0x1FFFF800: "OPTION BYTES — RDP!",
    0x1FFFF7E0: "DEVICE_ID",
    0x1FFFF7E8: "UID",
    0xE0042004: "DBGMCU_CR — DBG_SLEEP!",
    0xE0042000: "DBGMCU_IDCODE",
    0x40007000: "PWR_CR — STOP!",
    0x40007004: "PWR_CSR",
    0xE000ED10: "SCB SCR — SLEEPDEEP!",
    0xE000EDF0: "DHCSR",
    0xE000EDFC: "DEMCR",
    0xE0002000: "FP_CTRL",
    0xE0002008: "FP_COMP0",
    0xE0002010: "FP_COMP2",
    0xE0002018: "FP_COMP4",
    0xE0002020: "FP_COMP6",
}

SWJ_BITS = 0x07000000


def ldr_refs(img, target):
    """(pool_addr, ldr_addr) с ТОЧНЫМ декодированием LDR Rd,[PC,#imm]."""
    n = len(img)
    pools = [BASE + off for off in range(0, n - 3, 4)
             if struct.unpack_from("<I", img, off)[0] == target]
    if not pools:
        return [], []
    pset = set(pools)
    refs = []
    for off in range(0, n - 1, 2):
        hw = struct.unpack_from("<H", img, off)[0]
        if 0x4800 <= hw <= 0x4FFF:
            pc = BASE + off
            lit = ((pc + 4) & ~3) + (hw & 0xFF) * 4
            if lit in pset:
                refs.append(pc)
    return pools, refs


def disasm_at(img, addr, count=18):
    off = addr - BASE
    out = []
    for ins in md.disasm(img[off:off + count * 4 + 8], addr):
        ann = ""
        for tok in ins.op_str.replace(",", " ").split():
            tok = tok.strip("[]!#")
            if tok.startswith("0x"):
                try:
                    v = int(tok, 16)
                except ValueError:
                    continue
                if v in WATCH:
                    ann = f"   ; {WATCH[v]}"
                if (v & SWJ_BITS) and ins.mnemonic != "ldr":
                    ann += f"   ; SWJ_CFG-биты {v:#x}!"
        out.append(f"    0x{ins.address:08X}: {ins.bytes.hex():10s} {ins.mnemonic:8s} {ins.op_str}{ann}")
        if len(out) >= count:
            break
    return "\n".join(out)


def scan(name, path):
    img = open(path, "rb").read()
    boot_end = 0x1198
    print("=" * 78)
    print(f"ОБРАЗ: {name}")
    total = 0
    for target, label in sorted(WATCH.items()):
        pools, refs = ldr_refs(img, target)
        if not pools:
            continue
        total += 1
        # регион находок
        regions = []
        for r in refs:
            regions.append("бут" if r - BASE < boot_end else "прил")
        print(f"\n  {label} @0x{target:08X}: {len(pools)} литерал(ов) в пулах "
              f"{['0x%08X' % p for p in pools[:6]]}, LDR-ссылок: {len(refs)} "
              f"({','.join(regions[:8])})")
        seen = set()
        for r in refs[:10]:
            print(f"  -- использование на 0x{r:08X} ({'бутлоадер' if r - BASE < boot_end else 'приложение'}):")
            print(disasm_at(img, r))
    # WFI/WFE
    for lo, hi, reg in ((0, boot_end, "бутлоадер"), (boot_end, len(img), "приложение")):
        cands = []
        for off in range(lo, min(hi, len(img) - 1), 2):
            hw = struct.unpack_from("<H", img, off)[0]
            if hw in (0xBF30, 0xBF20):
                cands.append((BASE + off, "WFI" if hw == 0xBF30 else "WFE"))
        print(f"\n  WFI/WFE в {reg}: {len(cands)} кандидат(ов): "
              + ", ".join(f"0x{a:08X}({k})" for a, k in cands[:15]))
        for a, k in cands[:3]:
            print(f"  -- контекст 0x{a:08X} {k}:")
            print(disasm_at(img, max(BASE, a - 16), 14))
    if total == 0:
        print("  литеральных ссылок на отладочные/защитные регистры НЕ НАЙДЕНО")
    print()


for n, p in IMAGES:
    scan(n, p)
print("ГОТОВО")
