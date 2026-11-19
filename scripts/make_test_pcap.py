#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_test_pcap.py — генерирует синтетический .pcapng в формате USBPcap
(LINKTYPE_USBPCAP=249) для самопроверки parse_usbpcap.py.

Моделирует фрагмент сеанса SM2: перечисление устройства (дескриптор устройства,
серийный номер), обмен командами 0x83 INFO / 0x88 ARM / 0x37 LAUNCH / 0x12 AUTH
и «зависание» устройства (нет ответа на AUTH — моделирует сценарий «00000»).
"""
import struct

def shb():
    body = struct.pack('<IHHq', 0x1A2B3C4D, 1, 0, -1)
    blk = struct.pack('<II', 0x0A0D0D0A, 8 + len(body) + 4) + body
    blk += struct.pack('<I', len(blk) + 4)
    return blk

def idb(linktype=249):
    body = struct.pack('<HHI', linktype, 0, 0xFFFF)
    body += struct.pack('<HHB', 9, 1, 6) + b'\x00' * 3   # if_tsresol = 6 (мкс)
    body += struct.pack('<HH', 0, 0)                      # opt_endofopt
    blk = struct.pack('<II', 0x00000001, 8 + len(body) + 4) + body
    blk += struct.pack('<I', len(blk) + 4)
    return blk

def epb(iface, tsec_us, data):
    ts_hi, ts_lo = (tsec_us >> 32) & 0xFFFFFFFF, tsec_us & 0xFFFFFFFF
    body = struct.pack('<IIIII', iface, ts_hi, ts_lo, len(data), len(data)) + data
    pad = (4 - (len(body) % 4)) % 4
    body += b'\x00' * pad
    blk = struct.pack('<II', 0x00000006, 8 + len(body) + 4) + body
    blk += struct.pack('<I', len(blk) + 4)
    return blk

def usbpcap(irp, status, function, info, bus, dev, ep, tr, data=b'', setup=None):
    if setup is not None:
        data = setup + data
    hdr = struct.pack('<HQIHBHHBBI', 27, irp, status, function, info,
                      bus, dev, ep, tr, len(data))
    return hdr + data

F_CTRL, F_BULK = 0x0008, 0x0009
T_CTRL, T_BULK = 2, 3

def main():
    out = shb() + idb()
    t = 1_000_000  # 1.0 c
    irp = 0x1000

    # 1. GET_DESCRIPTOR(DEVICE) — ответ устройства (IN, complete)
    devdesc = bytes([0x12, 0x01, 0x00, 0x02, 0xFF, 0x00, 0x00, 0x40,
                     0xA2, 0x20, 0x01, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01])
    setup = bytes([0x80, 0x06, 0x00, 0x01, 0x09, 0x04, 0x12, 0x00])  # GET_DESCRIPTOR(DEVICE): wValue=0x0100 LE, wIndex=0x0409, wLength=18
    out += epb(0, t, usbpcap(irp, 0, F_CTRL, 0x01, 1, 7, 0x00, T_CTRL,
                             data=devdesc, setup=setup))
    irp += 1

    # 2. GET_DESCRIPTOR(STRING idx=1) — серийный номер "A111788"
    serial = 'A111788'
    sdata = struct.pack('<BB', 2 + 2 * len(serial), 3) + serial.encode('utf-16-le')
    setup = bytes([0x80, 0x06, 0x01, 0x03, 0x09, 0x04, len(sdata), 0x00])  # GET_DESCRIPTOR(STRING idx=1): wValue=0x0301 LE
    t += 50_000
    out += epb(0, t, usbpcap(irp, 0, F_CTRL, 0x01, 1, 7, 0x00, T_CTRL,
                             data=sdata, setup=setup))
    irp += 1

    # 3. bulk OUT: 0x83 INFO (запрос)
    t += 950_000
    out += epb(0, t, usbpcap(irp, 0, F_BULK, 0x00, 1, 7, 0x02, T_BULK,
                             data=bytes([0x83] + [0x00] * 15)))
    irp += 1

    # 4. bulk IN: ответ INFO с серийником 0x0A111788
    t += 10_000
    out += epb(0, t, usbpcap(irp, 0, F_BULK, 0x01, 1, 7, 0x81, T_BULK,
                             data=bytes([0x83, 0x00] + list(struct.pack('<I', 0x0A111788)) + [0x00] * 10)))
    irp += 1

    # 5. bulk OUT: 0x88 ARM
    t += 490_000
    out += epb(0, t, usbpcap(irp, 0, F_BULK, 0x00, 1, 7, 0x02, T_BULK,
                             data=bytes([0x88] + [0x00] * 7)))
    irp += 1

    # 6. bulk IN: OK
    t += 50_000
    out += epb(0, t, usbpcap(irp, 0, F_BULK, 0x01, 1, 7, 0x81, T_BULK,
                             data=bytes([0x00] * 8)))
    irp += 1

    # 7. bulk OUT: 0x37 LAUNCH {ver=0x1198, crc=0x210E9A13, size=0x1353C}
    t += 450_000
    out += epb(0, t, usbpcap(irp, 0, F_BULK, 0x00, 1, 7, 0x02, T_BULK,
                             data=bytes([0x37]) + struct.pack('<HII', 0x1198, 0x210E9A13, 0x1353C)))
    irp += 1

    # 8. bulk IN: status=0 (запуск успешен)
    t += 50_000
    out += epb(0, t, usbpcap(irp, 0, F_BULK, 0x01, 1, 7, 0x81, T_BULK,
                             data=bytes([0x00] * 4)))
    irp += 1

    # 9. ПАУЗА 3.45 c, затем 0x12 AUTH — и ответа нет (сценарий «00000»)
    t += 3_450_000
    out += epb(0, t, usbpcap(irp, 0, F_BULK, 0x00, 1, 7, 0x02, T_BULK,
                             data=bytes([0x12] + list(range(1, 33)))))
    irp += 1

    # 10. пустой bulk IN (тайм-аут, данных нет)
    t += 2_000_000
    out += epb(0, t, usbpcap(irp, 0xC0000010, F_BULK, 0x01, 1, 7, 0x81, T_BULK))

    open('test_capture.pcapng', 'wb').write(out)
    print('OK: test_capture.pcapng (%d байт)' % len(out))

if __name__ == '__main__':
    main()
