#!/usr/bin/env python3
"""Поиск всех вызовов bootloader-сервисов (через literal 0x0800017C) в приложениях 2.21.35 и 2.22.3"""
import struct
from capstone import *

fw35 = open('/home/z/sm2pro/2.21.32/SM2_2.21.35_A71283.bin','rb').read()
fw22 = open('/home/z/sm2pro/2.21.32/firmware.bin','rb').read()
BASE = 0x08000000
md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)

SERVICE_NAMES = {
    0:'svc0: get serial?', 1:'svc1', 2:'svc2', 3:'svc3',
    4:'svc4: RESTART', 5:'svc5: ext-chip read', 6:'svc6: ext-chip write',
    7:'svc7: get build ID [0x08000180]', 8:'svc8: get key[idx] from 0x08000184',
    9:'svc9: CRC32 flash area', 10:'svc10: boot reason', 11:'svc11',
    12:'svc12', 13:'svc13: ext-chip transfer'
}

def find_svc_calls(d, region_start, region_end, label):
    """Ищем ldr rX, [pc, #imm] где literal = 0x0800017C, затем используем [rX] и blx"""
    print('#'*20, label, '#'*20)
    hits = []
    for off in range(region_start - BASE, region_end - BASE, 2):
        # ищем слово 0x0800017C в literal pool
        if struct.unpack_from('<I', d, off)[0] == 0x0800017C:
            addr = BASE + off
            # найдём ldr, ссылающийся на этот literal (в радиусе 4KB до)
            code_start = max(0, off - 0x400)
            for ins in md.disasm(d[code_start:off], BASE + code_start):
                if ins.mnemonic.startswith('ldr') and '[pc' in ins.op_str:
                    try:
                        imm = int(ins.op_str.split('#')[-1].rstrip(']').rstrip(), 0)
                        pc = (ins.address + 4) & ~3
                        if pc + imm == addr:
                            # это ldr reg, =0x0800017C; посмотрим, что дальше (в разумном окне)
                            nxt = list(md.disasm(d[ins.address-BASE:ins.address-BASE+80], ins.address))
                            txt = '  0x%08X: %s %s' % (ins.address, ins.mnemonic, ins.op_str)
                            seq = []
                            for j, i2 in enumerate(nxt[1:12]):
                                seq.append('%s %s' % (i2.mnemonic, i2.op_str))
                            hits.append((ins.address, ' ; '.join(seq[:6])))
                    except Exception:
                        pass
    for a, s in hits:
        print('  0x%08X: %s' % (a, s))
    print('итого обращений:', len(hits))
    print()
    return hits

# 2.21.35: приложение с 0x08005000 до 0x08020000 (конец по энтропии: 0x20000 в файле)
h35 = find_svc_calls(fw35, 0x08005000, 0x08020000, '2.21.35 (дистрибутив)')
# 2.22.3: приложение с 0x08005000 до 0x0801853C (последний не-FF)
h22 = find_svc_calls(fw22, 0x08005000, 0x0801853C, '2.22.3 (firmware.bin)')
