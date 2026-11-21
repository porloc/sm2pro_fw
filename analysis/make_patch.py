#!/usr/bin/env python3
"""Патч firmware.bin (2.22.3 клона): перенос крипто-таблицы из 2.21.35 (дистрибутив)
+ опционально PID 0002 в дескрипторе bootloader'а"""
import struct, sys

fw = bytearray(open('/home/z/sm2pro/2.21.32/firmware.bin','rb').read())       # 2.22.3 с адаптера (клон)
fw35 = open('/home/z/sm2pro/2.21.32/SM2_2.21.35_A71283.bin','rb').read()       # 2.21.35 с заполненной таблицей

# EEPROM-страница A: 0x08002800..0x08003000 (файл-смещения 0x2800..0x3000)
# Таблица авторизации: регистры 0x39..0xB8 → 0x08002872..0x08002970
# Копируем регистры 0x39..0xB8 (256 байт) из 2.21.35
src_off = 0x2800 + 0x39*2
dst_off = 0x2800 + 0x39*2
tbl = bytes(fw35[src_off:src_off + 128*2])
fw[dst_off:dst_off+256] = tbl
print('Таблица 0x39..0xB8 скопирована из 2.21.35:')
for i in range(0, 128, 16):
    print('  [%3d]: %s' % (i, ' '.join('%04x'%struct.unpack_from('<H', tbl, i*2+j)[0] for j in range(0,32,2))))

# Дополнительно: серийный/заголовок EEPROM (регистры 0x00..0x0F) НЕ трогаем (у клона свой CRC stage2!)

# Вариант с PID=0002 (дескриптор bootloader'а @0x0800271A+10, файл-смещение 0x271A+10=0x2724)
if len(sys.argv) > 1 and sys.argv[1] == 'pid2':
    struct.pack_into('<H', fw, 0x2724, 0x0002)
    print('PID изменён: 0x0001 -> 0x0002 (@0x08002724)')

out = sys.argv[2] if len(sys.argv) > 2 else '/home/z/sm2pro/firmware_2.22.3_patched_auth.bin'
open(out,'wb').write(bytes(fw))
print('Сохранено:', out, len(fw), 'байт')
