#!/usr/bin/env python3
"""Декодер USB-сессий SM2 Pro (USBPcap, Mass Storage BOT поверх vendor SCSI)"""
import struct, sys

def pkts(path):
    d = open(path,'rb').read()
    off = 0; out = []
    while off + 12 <= len(d):
        btype, blen = struct.unpack_from('<II', d, off)
        if btype == 0x0A0D0D0A: off += blen; continue
        if blen < 12 or blen > len(d): break
        if btype == 6:
            payload = d[off+8:off+blen-4]
            iface, ts_hi, ts_lo, caplen, origlen = struct.unpack_from('<IIIII', payload, 0)
            out.append(((ts_hi<<32)|ts_lo, payload[20:20+caplen]))
        off += blen
    return out

SCSI_NAMES = {
    0x00: 'TEST_UNIT_READY', 0x12: 'INQUIRY', 0x03: 'REQUEST_SENSE',
    0x28: 'READ10', 0x2A: 'WRITE10', 0x25: 'READ_CAPACITY',
    0x1B: 'START_STOP', 0x1E: 'MEDIA_REMOVAL', 0x23: 'READ_FORMAT',
    0x55: 'MODE_SELECT10', 0x5A: 'MODE_SENSE10', 0x15: 'MODE_SELECT6',
    0x1A: 'MODE_SENSE6', 0x35: 'SYNCH_CACHE', 0xA8: 'READ12', 0xAA: 'WRITE12',
}

def decode(path, label, out=None):
    lines = []
    ps = pkts(path)
    t0 = ps[0][0] if ps else 0
    state = {}  # ожидание данных IN для tag
    cur_cmd = None
    data_buf = {}  # tag -> bytes
    for ts, p in ps:
        if struct.unpack_from('<H', p, 0)[0] != 27: continue
        data = p[27:]
        ep = p[21]
        if data[:4] == b'USBC' and len(data) >= 31:
            tag, dlen = struct.unpack_from('<II', data, 4)
            flags, lun, cbl = data[12], data[13], data[14]
            cb = data[15:15+cbl]
            op = cb[0] if cb else -1
            name = SCSI_NAMES.get(op, 'VENDOR_%02X' % op)
            cur_cmd = (tag, dlen, flags, lun, cb, name)
            data_buf[tag] = b''
            lines.append('[%8.3f] CMD tag=%08X %s lun=%d dlen=%d flags=%02X cb=%s' % (
                (ts-t0)/1e6, tag, name, lun, dlen, flags, ' '.join('%02x'%b for b in cb)))
        elif data[:4] == b'USBS' and len(data) >= 13:
            tag = struct.unpack_from('<I', data, 4)[0]
            resid, status = struct.unpack_from('<IB', data, 8)
            # сопоставим с командой
            cb_s = ''
            if cur_cmd and cur_cmd[0] == tag:
                cb_s = cur_cmd[5]
            buf = data_buf.get(tag, b'')
            extra = ''
            if 0 < len(buf) <= 64:
                extra = ' data[%d]=%s' % (len(buf), ' '.join('%02x'%b for b in buf[:48]))
            elif buf:
                extra = ' data[%d]' % len(buf)
            lines.append('[%8.3f] CSW tag=%08X status=%d resid=%d%s%s' % (
                (ts-t0)/1e6, tag, status, resid, (' cb='+cb_s if cur_cmd and cur_cmd[0]==tag else ''), extra))
            data_buf.pop(tag, None)
        else:
            # данные data-phase
            if cur_cmd:
                tag = cur_cmd[0]
                data_buf[tag] = data_buf.get(tag, b'') + data
    print('#'*25, label, '#'*25)
    for l in lines:
        print(l)
    print()
    return lines

if __name__ == '__main__':
    decode('/home/z/sm2pro/2.21.32/sm2pro2.21.35.pcapng', '2.21.35 WORKING')
    decode('/home/z/sm2pro/2.21.32/sm2pro .pcapng', 'FAIL (2.22.3?)')
