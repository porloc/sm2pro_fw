#!/usr/bin/env python3
import struct
from capstone import *

fw = open('/home/z/sm2pro/2.21.32/firmware.bin','rb').read()
fw35 = open('/home/z/sm2pro/2.21.32/SM2_2.21.35_A71283.bin','rb').read()
BASE = 0x08000000
md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)

def w(off): return struct.unpack_from('<I', fw, off)[0]

def dis(d, addr, n_instr, label):
    print("======== %s @ 0x%08X ========" % (label, addr))
    off = addr - BASE
    code = d[off:off+n_instr*4+64]
    cnt = 0
    for ins in md.disasm(code, addr):
        line = "  0x%08X: %-8s %s" % (ins.address, ins.mnemonic, ins.op_str)
        if ins.mnemonic == 'ldr' and '[pc' in ins.op_str:
            try:
                imm = int(ins.op_str.split('#')[-1].rstrip(']').rstrip(), 0)
                pc = (ins.address + 4) & ~3
                lit = struct.unpack_from('<I', d, pc + imm - BASE)[0]
                line += "   ; =0x%08X" % lit
            except Exception:
                pass
        if ins.mnemonic in ('bl','blx','b','bw') and '#0x' in ins.op_str:
            try:
                t = int(ins.op_str.split('#')[1], 16)
                line += '  ; -> 0x%08X' % t
            except Exception:
                pass
        print(line)
        cnt += 1
        if cnt >= n_instr: break
    print()

def find_start(d, addr, maxback=0x600):
    best = None
    for back in range(2, maxback, 2):
        a = addr - back
        off = a - BASE
        if off < 0: break
        hw = struct.unpack_from('<H', d, off)[0]
        # push {..., lr}: B5xx; push.w: E92D xxxx (lr bit 0x4000)
        if (hw & 0xFF00) == 0xB500 or (hw & 0xFFFF) == 0xE92D:
            best = a
    return best

# Кто вызывает 0x08007E82-зону: найдём начала функций
f1 = find_start(fw, 0x08007E82)
f2 = find_start(fw, 0x08007EE2)
print('начало ф-ции вокруг 0x08007E82:', hex(f1) if f1 else None)
print('начало ф-ции вокруг 0x08007EE2:', hex(f2) if f2 else None)
print()

dis(fw, f1, 45, "EXT-CHIP READ fn (сервис 5)")
dis(fw, f2, 40, "EXT-CHIP WRITE fn (сервис 6)")
