#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Глубокое дизассемблирование функций sm2lib.dll 2.22.3 (без ранней остановки).

Использование:
  python3 dis_deep.py 0x1000BD00 [len]      — дизассемблер с адреса
  python3 dis_deep.py calls 0x1000BD00       — только вызовы/команды
Аннотации: строки .rdata, отправляемые команды (mov byte [r+0x24], imm),
вызовы известных функций.
"""
from capstone import *
import struct, sys

path = "/home/z/my-project/fw_analysis/new_dist/extracted/Scanmatik/sm2lib.dll"
d = open(path, "rb").read()
md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = True

SECS = [
    (0x1000,  0x3E436, 0x400),
    (0x40000, 0x33C6E, 0x3EA00),
    (0x74000, 0x83D0,  0x72800),
    (0x7D000, 0x80,    0x78400),
    (0x7E000, 0x568,   0x78600),
    (0x7F000, 0x3C44,  0x78C00),
]

def va2fo(va):
    rva = va - 0x10000000
    for vs, vsize, ro in SECS:
        if vs <= rva < vs + vsize:
            return ro + rva - vs
    return None

def read_str_a(va, maxlen=80):
    fo = va2fo(va)
    if fo is None: return None
    s = d[fo:fo+maxlen].split(b'\x00')[0]
    if len(s) < 3: return None
    try: return s.decode('cp1251')
    except: return None

def read_str_w(va, maxlen=80):
    fo = va2fo(va)
    if fo is None: return None
    raw = d[fo:fo+maxlen*2]
    txt = raw.split(b'\x00\x00')[0] + b'\x00'
    if len(txt) < 6: return None
    try: return txt.decode('utf-16-le', errors='replace')
    except: return None

KNOWN = {
    0x1000B9F0: "send_recv (обмен командой)",
    0x1000BB30: "cmd_0x83_INFO_boot",
    0x1000C760: "fill_update_records",
    0x1000C940: "stage1_update",
    0x1000CB70: "stage2_update",
    0x1000CD50: "connect_scenario (sm2lib_49)",
    0x1000C830: "check_skip_serial",
    0x1000FD80: "sm2lib_185 (?)",
    0x1000BD00: "sm2lib_45 open",
    0x1000C730: "sm2lib_148 info",
}

def dis(start_va, length=0x400):
    fo = va2fo(start_va)
    if fo is None:
        print(f"!! bad VA 0x{start_va:08X}")
        return
    code = d[fo:fo+length]
    print(f"===== func @ 0x{start_va:08X} (len 0x{length:X}) =====")
    for ins in md.disasm(code, start_va):
        extra = ""
        ops = ins.op_str
        # аннотация вызовов
        if ins.mnemonic in ('call', 'jmp') and ops.startswith('0x'):
            tgt = int(ops, 16)
            if tgt in KNOWN:
                extra = f"   ; << {KNOWN[tgt]}"
            else:
                s = read_str_a(tgt) or read_str_w(tgt)
                if s: extra = f'   ; "{s[:50]}"'
        # аннотация команд протокола: mov byte [reg+0x24], imm
        if ins.mnemonic == 'mov' and ins.operands and len(ins.operands) == 2:
            op0, op1 = ins.operands
            if op0.type == CS_OP_MEM and op0.mem.disp == 0x24 and op1.type == CS_OP_IMM:
                extra += f"   ; >>> OPCODE 0x{op1.imm:02X}"
            # mov word [r+0x25], imm — длина
            if op0.type == CS_OP_MEM and op0.mem.disp == 0x25 and op1.type == CS_OP_IMM:
                extra += f"   ; len=0x{op1.imm:X}"
        # аннотация строковых указателей в rdata
        for tok in ops.replace(',', ' ').split():
            if tok.startswith('0x'):
                try: v = int(tok, 16)
                except: continue
                if 0x10040000 <= v < 0x10074000:
                    s = read_str_w(v) or read_str_a(v)
                    if s and len(s) > 3:
                        extra += f'   ; str "{s[:60]}"'
        print(f"  0x{ins.address:08X}: {ins.bytes.hex():<20} {ins.mnemonic:<8} {ops}{extra}")

if __name__ == "__main__":
    if sys.argv[1].startswith('0x'):
        a = int(sys.argv[1], 16)
        n = int(sys.argv[2], 0) if len(sys.argv) > 2 else 0x400
        dis(a, n)
