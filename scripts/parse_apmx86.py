#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Парсер .apmx86 (API Monitor x86) для захватов smwin <-> Scanmatik.

Формат: текстовый заголовок 218 байт + ZIP {definitions, process/0/{info,calls,data}}.
- calls: массив u32 смещений записей в data
- запись: +0x008 индекс, +0x020 сайт вызова (смещение в модуле),
  +0x024 указатель API в базе определений (0x57281A=CreateFileW,
  0x579BD2=DeviceIoControl, 0x579F1A=CloseHandle), +0x038 u64 QPC (100 нс),
  +0x040 возвращаемое значение, +0x044 GetLastError.
- параметры сериализованы после заголовка; буферы инлайн:
  паттерн {u32 size, u32 addr, data[size]}.

Контрольная сумма протокола Sm2: byte3 == (b0+b1+b2+0x55) & 0xFF.
"""
import io
import struct
import sys
import zipfile

API_NAMES = {
    0x57281A: "CreateFileW",
    0x579BD2: "DeviceIoControl",
    0x579F1A: "CloseHandle",
}

# Известные команды Sm2 (первый байт)
CMD_NAMES = {
    0x12: "AUTH", 0x27: "CONFIG", 0x33: "33", 0x34: "34", 0x35: "35",
    0x36: "36", 0x37: "LAUNCH", 0x80: "ERASE", 0x81: "WRITE", 0x82: "END",
    0x83: "INFO", 0x84: "84", 0x85: "85", 0x86: "86", 0x87: "87",
    0x88: "ARM", 0x89: "89",
}


def load(path):
    d = open(path, "rb").read()
    z = zipfile.ZipFile(io.BytesIO(d[218:]))
    calls = z.read("process/0/calls")
    data = z.read("process/0/data")
    offs = struct.unpack(f"<{len(calls)//4}I", calls)
    return offs, data


def parse_record(rec):
    idx = struct.unpack_from("<I", rec, 8)[0]
    site = struct.unpack_from("<I", rec, 0x20)[0]
    api = struct.unpack_from("<I", rec, 0x24)[0]
    qpc = struct.unpack_from("<Q", rec, 0x38)[0]
    ret = struct.unpack_from("<i", rec, 0x40)[0]
    err = struct.unpack_from("<I", rec, 0x44)[0]
    return dict(idx=idx, site=site, api=api, qpc=qpc, ret=ret, err=err, rec=rec)


def find_blobs(rec):
    """Паттерн сериализации буфера API Monitor:
    {u32=1, u32=1, addr, u32=1, size, addr, data[size]} — addr дважды."""
    blobs = []
    n = len(rec)
    p = 0x48
    while p + 24 <= n:
        (a, b, addr, c, size, addr2) = struct.unpack_from("<IIIIII", rec, p)
        if (a == 1 and b == 1 and c == 1 and addr == addr2
                and 0x10000 <= addr < 0x80000000
                and 0 < size <= 0x8000 and p + 24 + size <= n):
            blobs.append((p + 8, addr, size, rec[p + 24:p + 24 + size]))
            p += 24 + size
            continue
        p += 1
    return blobs


def chk(b):
    return len(b) >= 4 and b[3] == (b[0] + b[1] + b[2] + 0x55) & 0xFF


def classify(blob):
    b = blob
    if len(b) >= 4 and chk(b):
        if b[0] in CMD_NAMES:
            return f"CMD 0x{b[0]:02X} {CMD_NAMES[b[0]]}"
        if b[0] == 0x00:
            return f"RESP status={b[1]:02X} len=0x{b[2]:02X}"
    return None


def parse_capture(path):
    offs, data = load(path)
    recs = []
    for i, o in enumerate(offs):
        end = offs[i + 1] if i + 1 < len(offs) else len(data)
        recs.append(parse_record(data[o:end]))
    t0 = recs[0]["qpc"] if recs else 0
    lines = []
    for r in recs:
        api = API_NAMES.get(r["api"], f"api@{r['api']:X}")
        t_ms = (r["qpc"] - t0) / 10000.0
        line = f"[{r['idx']:3d}] t={t_ms:9.1f}ms {api:16s} site=0x{r['site']:x} ret={r['ret']}"
        if r["err"]:
            line += f" err={r['err']}"
        lines.append(line)
        if api == "DeviceIoControl":
            for off, addr, size, blob in find_blobs(r["rec"]):
                cls = classify(blob)
                hx = " ".join(f"{x:02X}" for x in blob[:64])
                more = "…" if size > 64 else ""
                lines.append(f"        buf@0x{addr:08X}({size}B) @{off:#04x}: {hx}{more}"
                             + (f"   <-- {cls}" if cls else ""))
        elif api == "CreateFileW":
            # имя файла: UTF-16 строка в записи
            rec = r["rec"]
            s = rec.find(b"\\\x00.\x00\\\x00")
            if s >= 0:
                name = rec[s:s + 128].decode("utf-16-le", errors="replace").split("\x00")[0]
                lines.append(f"        open('{name}')")
    return lines, recs


if __name__ == "__main__":
    for path, tag in [(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "")]:
        lines, recs = parse_capture(path)
        print(f"===== {path} [{tag}]: {len(recs)} вызовов")
        for l in lines:
            print(l)
