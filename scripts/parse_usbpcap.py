#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
parse_usbpcap.py — транскриптор USBPcap-записей (Wireshark, LINKTYPE_USBPCAP=249)
для анализа обмена ПК-ПО Scanmatik / SM2 Pro J2534 с адаптером.

Превращает .pcapng/.pcap в читаемый протокол: перечисление USB (дескрипторы,
серийный номер), все bulk-пакеты «хост → устройство» / «устройство → хост»
с hex-дампом, аннотации известных команд протокола SM2, поиск маркеров
(серийник, версии, CRC), паузы >100 мс (признак тайм-аута) и итоговая
статистика.

Использование:
    python3 parse_usbpcap.py capture.pcapng                     # транскрипт на экран
    python3 parse_usbpcap.py capture.pcapng -o report.txt       # транскрипт в файл
    python3 parse_usbpcap.py capture.pcapng --json events.json  # машинный JSON
    python3 parse_usbpcap.py capture.pcapng --dev 7             # только устройство №7
    python3 parse_usbpcap.py capture.pcapng --bulk-only         # только bulk-обмен

Зависимости: только стандартная библиотека Python 3.
"""

import argparse
import json
import struct
import sys

LINKTYPE_USBPCAP = 249
USBPCAP_HDR_LEN = 27

TR_ISOC, TR_INTR, TR_CTRL, TR_BULK = 0, 1, 2, 3
TR_NAMES = {TR_ISOC: 'ISOC', TR_INTR: 'INTR', TR_CTRL: 'CTL ', TR_BULK: 'BULK'}

INFO_IN = 0x01        # данные идут устройство → хост
INFO_PSEUDO = 0x02    # псевдо-регистры (служебное USBPcap, не USB-данные)

# ----------------------------------------------------------------------------
# Известные команды протокола SM2 (первый байт bulk-пакета; эвристика —
# фрейминг протокола уточнится по «золотому» логу).
# ----------------------------------------------------------------------------
CMD_NAMES = {
    # бутлоадер 0x80–0x8B
    0x82: 'бутлоадер: опрос поколения (ответ 0x18/1 = новое поколение)',
    0x83: 'бутлоадер: INFO (серийник / версия / тип)',
    0x88: 'бутлоадер: ARM (запуск образа по 0x08004000)',
    0x8B: 'запись данных нового поколения (0x68 байт)',
    # стаб 0x33–0x37
    0x37: 'стаб: LAUNCH {ver, crc, size} → запуск приложения',
    # приложение (по таблице команд реверса 2.22.3)
    0x12: 'приложение: AUTH (аутентификация)',
    0x27: 'приложение: CONFIG (EEPROM-слоты 0x38–0xB8)',
}
CMD_RANGES = (
    (0x80, 0x8A, 'бутлоадер 0x%02X'),
    (0x33, 0x36, 'стаб 0x%02X'),
)

def annot_cmd(b):
    if b in CMD_NAMES:
        return CMD_NAMES[b]
    for lo, hi, fmt in CMD_RANGES:
        if lo <= b <= hi:
            return fmt % b
    return None

# Маркеры, которые ищем в bulk-данных (известные константы связки SM2)
MARKERS = [
    ('serial 0x0A111788 (донор A111788)', bytes.fromhex('8817110a')),
    ('ver 0x1198 (прошивка 2.22.3)',      bytes.fromhex('9811')),
    ('crc app 0x210E9A13 (2.22.3)',       bytes.fromhex('139a0e21')),
    ('size app 0x1353C (2.22.3)',         bytes.fromhex('3c350100')),
    ('seed стаба 0x7821AB35',             bytes.fromhex('35ab2178')),
    ('crc стаба 0x2912D0A0',              bytes.fromhex('a0d01229')),
    ('size стаба 0xB00',                  bytes.fromhex('000b0000')),
    ('ver 0x1070 (прошивка 2.21.32)',     bytes.fromhex('7010')),
]

REQ_NAMES = {
    0x00: 'GET_STATUS', 0x05: 'SET_ADDRESS', 0x06: 'GET_DESCRIPTOR',
    0x09: 'SET_CONFIGURATION', 0x08: 'SET_CONFIGURATION?',
    0x0A: 'GET_INTERFACE', 0x0B: 'SET_INTERFACE', 0x01: 'CLEAR_FEATURE',
}

DESC_NAMES = {1: 'DEVICE', 2: 'CONFIG', 3: 'STRING', 6: 'DEVICE_QUALIFIER'}

# ----------------------------------------------------------------------------
# Чтение форматов
# ----------------------------------------------------------------------------

def read_pcapng(data):
    """Возвращает список (iface, tsec, bytes) и словарь интерфейсов."""
    packets, ifaces = [], {}
    endian, off, n = '<', 0, len(data)
    while off + 12 <= n:
        btype, blen = struct.unpack_from(endian + 'II', data, off)
        if blen < 12 or off + blen > n:
            break
        body = data[off + 8:off + blen - 4]
        if btype == 0x0A0D0D0A:  # Section Header Block
            magic = struct.unpack_from('<I', body, 0)[0]
            endian = '<' if magic == 0x1A2B3C4D else '>'
        elif btype == 0x00000001:  # Interface Description Block
            linktype = struct.unpack_from(endian + 'H', body, 0)[0]
            tsr = 6  # по умолчанию микросекунды
            o = 8
            while o + 4 <= len(body):
                code, olen = struct.unpack_from(endian + 'HH', body, o)
                if code == 0:
                    break
                val = body[o + 4:o + 4 + olen]
                if code == 9 and olen >= 1:  # if_tsresol
                    b = val[0]
                    tsr = -(b & 0x7F) if (b & 0x80) else b
                o += 4 + ((olen + 3) & ~3)
            ifaces[len(ifaces)] = {'link': linktype, 'tsresol': tsr}
        elif btype == 0x00000006:  # Enhanced Packet Block
            iface, ts_hi, ts_lo, caplen, origlen = struct.unpack_from(
                endian + 'IIIII', body, 0)
            pkt = body[20:20 + caplen]
            info = ifaces.get(iface, {'link': LINKTYPE_USBPCAP, 'tsresol': 6})
            ts = ((ts_hi << 32) | ts_lo)
            tsr = info['tsresol']
            tsec = ts / (10 ** tsr) if tsr >= 0 else ts * (2.0 ** tsr)
            packets.append((iface, tsec, pkt))
        elif btype == 0x00000003:  # Simple Packet Block
            packets.append((0, None, body))
        # прочие блоки пропускаем
        off += blen
    return packets, ifaces


def read_pcap(data):
    """Классический libpcap. Возвращает список (iface, tsec, bytes)."""
    m = data[:4]
    if m == b'\xd4\xc3\xb2\xa1':
        endian, ns = '<', False
    elif m == b'\xa1\xb2\xc3\xd4':
        endian, ns = '>', False
    elif m == b'\x4d\x3c\xb2\xa1':
        endian, ns = '<', True
    elif m == b'\xa1\xb2\x3c\x4d':
        endian, ns = '>', True
    else:
        raise ValueError('Не pcap-файл')
    linktype = struct.unpack_from(endian + 'I', data, 20)[0] & 0xFFFF
    if linktype != LINKTYPE_USBPCAP:
        sys.stderr.write('Предупреждение: linktype=%d (ожидался 249)\n' % linktype)
    packets, off = [], 24
    while off + 16 <= len(data):
        ts, tf, caplen, _ = struct.unpack_from(endian + 'IIII', data, off)
        pkt = data[off + 16:off + 16 + caplen]
        packets.append((0, ts + (tf / 1e9 if ns else tf / 1e6), pkt))
        off += 16 + caplen
    return packets

# ----------------------------------------------------------------------------
# Разбор заголовка USBPcap
# ----------------------------------------------------------------------------

def parse_usbpcap(pkt):
    if len(pkt) < USBPCAP_HDR_LEN:
        return None
    hdr_len = struct.unpack_from('<H', pkt, 0)[0]
    if hdr_len < USBPCAP_HDR_LEN:
        return None
    irp_id = struct.unpack_from('<Q', pkt, 2)[0]
    status = struct.unpack_from('<I', pkt, 10)[0]
    function = struct.unpack_from('<H', pkt, 14)[0]
    info = pkt[16]
    bus, dev = struct.unpack_from('<HH', pkt, 17)
    ep = pkt[21]
    tr = pkt[22]
    dlen = struct.unpack_from('<I', pkt, 23)[0]
    payload = pkt[USBPCAP_HDR_LEN:USBPCAP_HDR_LEN + dlen]
    setup = None
    if tr == TR_CTRL and len(payload) >= 8:
        setup, payload = payload[:8], payload[8:]
    return {
        'irp': irp_id, 'status': status, 'function': function, 'info': info,
        'bus': bus, 'dev': dev, 'ep': ep, 'tr': tr, 'dlen': dlen,
        'payload': payload, 'setup': setup,
    }

# ----------------------------------------------------------------------------
# Оформление
# ----------------------------------------------------------------------------

def hexdump(b, indent='      '):
    lines = []
    for i in range(0, len(b), 16):
        chunk = b[i:i + 16]
        hexs = ' '.join('%02X' % c for c in chunk)
        asc = ''.join(chr(c) if 32 <= c < 127 else '.' for c in chunk)
        lines.append('%s%04X  %-47s  |%s|' % (indent, i, hexs, asc))
    return lines


def setup_str(setup):
    rt, rq = setup[0], setup[1]
    wv, wi, wl = struct.unpack_from('<HHH', setup, 2)
    name = REQ_NAMES.get(rq, 'bRequest=%02X' % rq)
    if rq == 0x06:  # GET_DESCRIPTOR
        dtype, idx = (wv >> 8) & 0xFF, wv & 0xFF
        name = 'GET_DESCRIPTOR(%s idx=%d)' % (DESC_NAMES.get(dtype, hex(dtype)), idx)
    return rt, rq, wv, wi, wl, name


def analyze(packets, out, dev_filter=None, bulk_only=False, pause=0.1):
    events = []
    devices = {}          # (bus,dev) -> {'vid','pid','serial'}
    stats = {'h2d': 0, 'd2h': 0, 'h2d_bytes': 0, 'd2h_bytes': 0, 'other': 0}
    opcode_hist = {}
    prev_t = None
    t0 = None
    idx = 0
    total = len(packets)
    out.write('Разобрано пакетов USBPcap: %d\n' % total)
    out.write('=' * 78 + '\n')

    for iface, tsec, pkt in packets:
        if tsec is None:
            continue
        u = parse_usbpcap(pkt)
        if u is None:
            continue
        if t0 is None:
            t0 = tsec
        rel = tsec - t0

        # пауза между «содержательными» пакетами
        interesting = (u['dlen'] > 0 and not (u['info'] & INFO_PSEUDO))
        if interesting and prev_t is not None and (tsec - prev_t) > pause:
            out.write('-------- пауза %.6f с --------\n' % (tsec - prev_t))
        if interesting:
            prev_t = tsec

        if dev_filter is not None and u['dev'] not in (0, dev_filter):
            continue

        idx += 1
        ts = '[+%10.6f]' % rel
        hdr = '#%-5d %s ' % (idx, ts)

        # --- служебные пакеты USBPcap (конфигурация драйвера) ---
        if u['info'] & INFO_PSEUDO:
            if bulk_only or u['dlen'] == 0:
                continue
            out.write('%s ДРАЙВЕР bus=%d dev=%d func=0x%04X псевдоданные %d байт\n'
                      % (hdr, u['bus'], u['dev'], u['function'], u['dlen']))
            for ln in hexdump(u['payload'][:64]):
                out.write(ln + '\n')
            stats['other'] += 1
            continue

        # --- control-передачи (перечисление и т.п.) ---
        if u['tr'] == TR_CTRL:
            if u['dlen'] == 0:
                if not bulk_only and u['setup'] is None:
                    out.write('%s CTL    bus=%d dev=%d (status)\n' % (hdr, u['bus'], u['dev']))
                continue
            if u['setup'] is not None:
                rt, rq, wv, wi, wl, name = setup_str(u['setup'])
                direction = 'D→H' if (rt & 0x80) else 'H→D'
                line = '%s CTL %s bus=%d dev=%d %s' % (hdr, direction, u['bus'], u['dev'], name)
                data = u['payload']
                # расшифровка дескрипторов
                key = (u['bus'], u['dev'])
                if rq == 0x06 and len(data) >= 2:
                    dtype = (wv >> 8) & 0xFF
                    if dtype == 1 and len(data) >= 18:
                        vid, pid = struct.unpack_from('<HH', data, 8)
                        d = devices.setdefault(key, {})
                        d['vid'], d['pid'] = '0x%04X' % vid, '0x%04X' % pid
                        line += ' → VID=%s PID=%s class=%02X iSerial=%d' % (
                            d['vid'], d['pid'], data[4], data[16])
                    elif dtype == 3 and data[1] == 3:
                        try:
                            s = data[2:data[0]].decode('utf-16-le')
                            d = devices.setdefault(key, {})
                            d['serial'] = s
                            line += ' → "%s"' % s
                        except Exception:
                            pass
                if data:
                    line += ' (%d байт)' % len(data)
                out.write(line + '\n')
                if data and not bulk_only:
                    for ln in hexdump(data):
                        out.write(ln + '\n')
                events.append({'i': idx, 't': rel, 'kind': 'ctrl',
                               'bus': u['bus'], 'dev': u['dev'],
                               'req': name, 'dir': direction,
                               'data': data.hex()})
            stats['other'] += 1
            continue

        # --- bulk / interrupt ---
        if u['tr'] in (TR_BULK, TR_INTR) and u['dlen'] > 0:
            d2h = bool(u['info'] & INFO_IN)
            direction = 'D→H' if d2h else 'H→D'
            data = u['payload']
            hint = annot_cmd(data[0]) if data else None
            line = '%s %s bus=%d dev=%d ep=%02X %s %dB' % (
                hdr, direction, u['bus'], u['dev'], u['ep'],
                TR_NAMES[u['tr']], len(data))
            if hint:
                line += '  [%s]' % hint
            out.write(line + '\n')
            for ln in hexdump(data):
                out.write(ln + '\n')
            if d2h:
                stats['d2h'] += 1
                stats['d2h_bytes'] += len(data)
            else:
                stats['h2d'] += 1
                stats['h2d_bytes'] += len(data)
                if data:
                    opcode_hist[data[0]] = opcode_hist.get(data[0], 0) + 1
            events.append({'i': idx, 't': rel, 'kind': 'bulk',
                           'bus': u['bus'], 'dev': u['dev'], 'ep': u['ep'],
                           'dir': direction, 'data': data.hex(),
                           'hint': hint})
            continue

        # --- всё остальное (пустые/статусные) ---
        if not bulk_only and u['dlen'] > 0:
            out.write('%s %s    bus=%d dev=%d ep=%02X %s %dB (status=0x%08X)\n'
                      % (hdr, TR_NAMES.get(u['tr'], '????'), u['bus'], u['dev'],
                         u['ep'], u['tr'], u['dlen'], u['status']))
            stats['other'] += 1

    # ------------------------------------------------------------------ итог
    out.write('=' * 78 + '\nИТОГИ\n')
    for key in sorted(devices):
        d = devices[key]
        out.write('  устройство bus=%d dev=%d: VID=%s PID=%s serial=%s\n'
                  % (key[0], key[1], d.get('vid', '?'), d.get('pid', '?'),
                     d.get('serial', '?')))
    out.write('  хост→устройство : %d пакетов, %d байт\n' % (stats['h2d'], stats['h2d_bytes']))
    out.write('  устройство→хост : %d пакетов, %d байт\n' % (stats['d2h'], stats['d2h_bytes']))
    if opcode_hist:
        out.write('  гистограмма кодов первых байт H→D (top-20):\n')
        for op, cnt in sorted(opcode_hist.items(), key=lambda kv: -kv[1])[:20]:
            hint = annot_cmd(op) or ''
            out.write('      0x%02X  ×%d  %s\n' % (op, cnt, hint))

    # ---------------------------------------------------------------- маркеры
    out.write('  маркеры (известные константы) в bulk-данных:\n')
    found_any = False
    for ev in events:
        if ev['kind'] != 'bulk':
            continue
        blob = bytes.fromhex(ev['data'])
        for name, pat in MARKERS:
            off = blob.find(pat)
            while off != -1:
                found_any = True
                out.write('      #%d [+%.6f] %s %s @ offset %d\n'
                          % (ev['i'], ev['t'], ev['dir'], name, off))
                off = blob.find(pat, off + 1)
    if not found_any:
        out.write('      (маркеры не найдены)\n')
    if prev_t is not None and t0 is not None:
        out.write('  длительность записи: %.3f с\n' % (prev_t - t0))
    return events


def main():
    ap = argparse.ArgumentParser(description='Транскриптор USBPcap-логов SM2 Pro')
    ap.add_argument('capture', help='файл .pcapng / .pcap, записанный Wireshark+USBPcap')
    ap.add_argument('-o', '--output', help='выходной текстовый файл (по умолчанию stdout)')
    ap.add_argument('--json', help='дополнительно выгрузить события в JSON')
    ap.add_argument('--dev', type=int, help='показывать только устройство с этим адресом')
    ap.add_argument('--bulk-only', action='store_true', help='только bulk-обмен')
    ap.add_argument('--pause', type=float, default=0.1, help='порог паузы, с (0.1)')
    args = ap.parse_args()

    data = open(args.capture, 'rb').read()
    if data[:4] == b'\x0a\x0d\x0d\x0a':
        packets, _ifaces = read_pcapng(data)
    else:
        packets = read_pcap(data)
    if not packets:
        sys.stderr.write('Пакеты не найдены — файл другого формата?\n')
        sys.exit(1)

    out = open(args.output, 'w', encoding='utf-8') if args.output else sys.stdout
    try:
        events = analyze(packets, out, dev_filter=args.dev,
                         bulk_only=args.bulk_only, pause=args.pause)
    finally:
        if args.output:
            out.close()
    if args.json:
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump(events, f, ensure_ascii=False, indent=1)
    if args.output:
        print('Готово: %s' % args.output)


if __name__ == '__main__':
    try:
        main()
    except BrokenPipeError:
        # вывод оборван (напр. `| head`) — это не ошибка разбора
        try:
            sys.stdout.close()
        except Exception:
            pass
