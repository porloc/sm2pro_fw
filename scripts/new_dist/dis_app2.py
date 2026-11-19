#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Дизассемблер приложения 2.22.3 с разрешением pc-литералов и аннотациями."""
from capstone import *
from capstone.arm import ARM_REG_PC
import struct, sys

APP = "/home/z/my-project/fw_analysis/new_dist/dec_sm2_entry2.bin"
data = open(APP, "rb").read()
BASE = 0x08005000
md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
md.detail = True

# известные адреса
KNOWN = {
    0x0800017C: "ptr_таблицы_сервисов_бутлоадера",
    0x08000180: "серийный номер",
    0x08000184: "крипто-блоб +0x184",
    0x08002800: "EEPROM стр.1",
    0x080028E8: "вирт. UID",
    0x08018338: "таблица пинов (режим 1)",
    0x080183C9: "таблица пинов (режим 2/3)",
    0x0801823C: "таблица протоколов (240*?)",
    0x0800C2CA: "диспетчер обфускации",
    0x0800C15C: "крипто-ядро",
    0x0800C520: "пул UID (auth)",
    0x40021000: "RCC",
    0x40010800: "GPIOA",
    0x40011000: "GPIOC",
    0x40011400: "GPIOD",
    0x40011800: "GPIOE",
    0x40005C00: "USB PMEM?",
    0x40006000: "USB",
    0xE000E010: "SysTick",
    0xE000E100: "NVIC",
    0x20000000: "SRAM",
    0x1FFFF7E8: "UID кристалла",
    0x1FFFF7E0: "UID+0",
    0x1FFFF7EC: "UID+4",
}

def lit_val(addr):
    off = addr - BASE
    if 0 <= off <= len(data)-4:
        return struct.unpack_from('<I', data, off)[0]
    return None

def dis(addr, size, title=""):
    off = addr - BASE
    if off < 0 or off >= len(data):
        print(f"!! 0x{addr:08X} вне диапазона")
        return
    print(f"--- {title} @ 0x{addr:08X} ---")
    for ins in md.disasm(data[off:off+size], addr):
        extra = ""
        # разрешение pc-литералов
        if ins.mnemonic.startswith('ldr') and 'pc' in ins.op_str:
            for op in ins.operands:
                if op.type == CS_OP_MEM and op.mem.base == ARM_REG_PC:
                    lit_addr = (ins.address + 4 + op.mem.disp) & ~3
                    v = lit_val(lit_addr)
                    if v is not None:
                        ann = KNOWN.get(v)
                        if 0x08005000 <= v < 0x08005000+len(data):
                            ann = f"app+0x{v-0x08005000:X}"
                        elif 0x08000000 <= v < 0x08040000:
                            ann = ann or f"флеш 0x{v:08X}"
                        elif 0x40000000 <= v < 0x40080000:
                            ann = ann or f"периферия"
                        elif 0xE0000000 <= v:
                            ann = ann or "PPB"
                        extra = f"   ; [0x{lit_addr:08X}] = 0x{v:08X}" + (f" ({ann})" if ann else "")
        # адреса переходов
        if ins.mnemonic in ('bl', 'b', 'blx') and ins.op_str.startswith('#'):
            try:
                tgt = int(ins.op_str[1:], 16)
                if tgt in KNOWN:
                    extra += f"   ; {KNOWN[tgt]}"
            except: pass
        print(f"  0x{ins.address:08X}: {ins.bytes.hex():<12} {ins.mnemonic:<10} {ins.op_str}{extra}")
    print()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].startswith('0x'):
        a = int(sys.argv[1], 16)
        n = int(sys.argv[2], 0) if len(sys.argv) > 2 else 0x80
        dis(a, n, "запрошено")
