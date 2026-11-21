#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверка отличающегося слова 0x0800E958: точная дизассемблировка + поиск всех ссылок."""
from capstone import *
import struct

DIR = "/home/z/my-project/fw_analysis/"
donor = open(DIR + "SM2_2.21.32_A111788_STM32F105VCT6.bin", "rb").read()
official = open(DIR + "SM2Pro_full_flash_2.21.32_restored.bin", "rb").read()

FLASH_BASE = 0x08000000
md = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_MCLASS)
md.detail = True
WORD_ADDR = 0x0800E958

def disasm(data, start_off, end_off, title):
    """start_off/end_off — файловые смещения == смещения от FLASH_BASE."""
    print(f"--- {title} (0x{FLASH_BASE+start_off:08X}..0x{FLASH_BASE+end_off:08X}) ---")
    for ins in md.disasm(data[start_off:end_off], FLASH_BASE + start_off):
        marker = ""
        if ins.address <= WORD_ADDR < ins.address + ins.size:
            marker = "   <<< СЛОВО-ОТЛИЧИЕ"
        print(f"  0x{ins.address:08X}: {ins.bytes.hex():<14} {ins.mnemonic:<10} {ins.op_str}{marker}")
    print()

# Функция начинается с 0x0800E88E (PUSH с LR найден ранее)
disasm(donor, 0x0E88E, 0x0E9A0, "ДОНОР: функция с 0x0800E88E")
disasm(official, 0x0E88E, 0x0E9A0, "ОФИЦИАЛЬНЫЙ: та же функция")
