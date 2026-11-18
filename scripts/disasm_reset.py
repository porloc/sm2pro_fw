#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ручная дизассемблировка reset handler и векторных целей бутлоадера через capstone."""
from capstone import *
import struct

BIN = "/home/z/my-project/fw_analysis/SM2_2.21.32_A111788_STM32F105VCT6.bin"
FLASH_BASE = 0x08000000
data = open(BIN, "rb").read()

md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
md.detail = False

def disasm(addr, size, title=""):
    off = addr - FLASH_BASE
    print(f"--- {title} @ 0x{addr:08X} ---")
    for ins in md.disasm(data[off:off+size], addr):
        print(f"  0x{ins.address:08X}: {ins.bytes.hex():<10} {ins.mnemonic:<8} {ins.op_str}")
    print()

# Reset handler
disasm(0x0800032C, 0x24, "Reset Handler")
# Стаб-обработчики
disasm(0x08000334, 0x20, "NMI/HardFault/default stubs")
# Что после векторной таблицы
disasm(0x08000130, 0xE0, "После векторной таблицы (0x118+)")

# Цели активных IRQ
for name, a in [("DMA1_CH6 IRQ", 0x08001D7A), ("DMA1_CH7 IRQ", 0x08001DB2),
                ("ADC1_2 IRQ", 0x080023C0), ("RTCAlarm IRQ", 0x08001BE0)]:
    disasm(a, 0x30, name)
