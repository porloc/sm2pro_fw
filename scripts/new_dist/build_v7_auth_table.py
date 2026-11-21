#!/usr/bin/env python3
"""build_v7_auth_table.py — сборка образов AUTH_TABLE v2 (таблица 2.21.35 + слоты LAUNCH + опц. PID 0002).

Исправления относительно первой сборки:
 1) PID пишем в idProduct @0x0800271C (device-дескриптор @0x08002712),
    а НЕ @0x08002724 (там заголовок конфиг-дескриптора 09 02 — старый патч
    ломал перечисление USB);
 2) после копирования таблицы regs 0x39–0xB8 из 2.21.35 возвращаем слоты
    LAUNCH @0x2886–0x2891 {size,ver,crc} — они ПЕРЕКРЫВАЮТ регион таблицы
    (regs 0x43–0x48), без них стаб 2.22.3 возвращает 7 → экранная [0007].

База: SM2Pro_full_flash_2.22.3_patched_v2_SWDON.bin (SWD жив после LAUNCH).
Выход:
  patched/firmware_2.22.3_AUTH_TABLE.bin        (PID 0001, контрольный)
  patched/firmware_2.22.3_AUTH_TABLE+PID2.bin   (PID 0002, главный кандидат)
"""
import hashlib, struct, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
FW = os.path.join(ROOT, "firmware")

BASE = os.path.join(FW, "SM2Pro_full_flash_2.22.3_patched_v2_SWDON.bin")   # SWDON
DONOR22135 = os.path.join(FW, "fw_22135.bin")                              # рабочий дамп 2.21.35

# ожидаемые хэши собранных образов (v2)
EXPECT = {
    "AUTH_TABLE":      "924e822a084c75ed647dcda75f2b0682",
    "AUTH_TABLE+PID2": "eda8eeb7459fee7a6cd0e11854c10159",
}

# слоты LAUNCH: {size=0x0001353C, ver=0x00001198, crc=0x210E9A13}
SLOTS = struct.pack("<HHHHHH", 0x353C, 0x0001, 0x1198, 0x0000, 0x9A13, 0x210E)
TBL_OFF, TBL_LEN = 0x2872, 0x100   # regs 0x39..0xB8 (128 halfword)
PID_OFF = 0x271C                   # idProduct в device-дескрипторе @0x2712

def build(pid2: bool) -> bytearray:
    base = bytearray(open(BASE, "rb").read())
    d35 = open(DONOR22135, "rb").read()
    assert len(base) == 0x40000 and len(d35) == 0x40000
    # 1) таблица regs 0x39–0xB8 из 2.21.35 (побайтово, включая слово @0x28E8)
    base[TBL_OFF:TBL_OFF+TBL_LEN] = d35[TBL_OFF:TBL_OFF+TBL_LEN]
    # 2) слоты LAUNCH (regs 0x43–0x48 — внутри региона таблицы!)
    base[0x2886:0x2892] = SLOTS
    # 3) PID 0x0002 в idProduct (дескриптор НЕ трогаем больше нигде)
    if pid2:
        assert base[0x2724:0x2726] == b"\x09\x02"
        base[PID_OFF:PID_OFF+2] = b"\x02\x00"
    return base

def verify(img: bytearray, pid2: bool):
    d35 = open(DONOR22135, "rb").read()
    def u16(o): return struct.unpack_from("<H", img, o)[0]
    def u32(o): return struct.unpack_from("<I", img, o)[0]
    checks = {
        "idVendor 0x20A2": u16(0x271A) == 0x20A2,
        "idProduct": u16(0x271C) == (0x0002 if pid2 else 0x0001),
        "conf header 09 02": img[0x2724:0x2726] == b"\x09\x02",
        "conf len 0x20": u16(0x2726) == 0x0020,
        "slots size": u32(0x2886) == 0x0001353C,
        "slots ver": u32(0x288A) == 0x00001198,
        "slots crc": u32(0x288E) == 0x210E9A13,
        "magic A 0x5AA5": u16(0x2FFE) == 0x5AA5,
        "bootrec ver 0x1198": u16(0x2804) == 0x1198,
        # таблица = 22135 ВЕЗДЕ, КРОМЕ ячеек слотов (regs 0x43-0x48 — туда пишем LAUNCH-параметры)
        "table==22135 (без слотов)": (
            bytes(img[TBL_OFF:0x2886]) == d35[TBL_OFF:0x2886] and
            bytes(img[0x2892:TBL_OFF+TBL_LEN]) == d35[0x2892:TBL_OFF+TBL_LEN]),
        "word@28E8=0x05D1FF35": u32(0x28E8) == 0x05D1FF35,
        "SWD keep @0xE1C": u32(0xE1C) == 0x7100F041,
        "serial 0x0A111788": u32(0x180) == 0x0A111788,
        "page B clean": all(b == 0xFF for b in img[0x3000:0x3800]),
    }
    bad = [k for k, v in checks.items() if not v]
    return bad

def main():
    ok_all = True
    for pid2, name, out in ((False, "AUTH_TABLE", "patched/firmware_2.22.3_AUTH_TABLE.bin"),
                            (True,  "AUTH_TABLE+PID2", "patched/firmware_2.22.3_AUTH_TABLE+PID2.bin")):
        img = build(pid2)
        bad = verify(img, pid2)
        md5 = hashlib.md5(bytes(img)).hexdigest()
        exp = EXPECT[name]
        match = "OK" if md5 == exp else f"MISMATCH (expect {exp})"
        print(f"{name}: {len(img)}B  MD5 {md5}  [{match}]  verify: {'PASS' if not bad else 'FAIL '+str(bad)}")
        if bad or md5 != exp:
            ok_all = False
            continue
        outp = os.path.join(ROOT, out)
        open(outp, "wb").write(bytes(img))
        print(f"  -> записан {outp}")
        if pid2:
            canon = os.path.join(FW, "SM2Pro_full_flash_2.22.3_AUTH_TABLE+PID2_v2.bin")
            open(canon, "wb").write(bytes(img))
            print(f"  -> записан {canon}")
    sys.exit(0 if ok_all else 1)

if __name__ == "__main__":
    main()
