#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Сборка диагностического образа v5: AUTH_BYPASS (2025-11-19, после API-лога 2.22.3).

Контекст (docs/APIMON2_ANALYSIS.md): захват API Monitor №2 доказал, что транспорт
и цепочка запуска работают идеально — INFO 0x83 (версия 0x1198 из EEPROM — фикс v2
работает, [0007] мёртв) → ARM 0x88 OK → LAUNCH 0x37 {0x1198, 0x210E9A13, 0x1353C}
OK — но запустившееся приложение 2.22.3 МОЛЧИТ на команду 0x12 AUTH (новый формат:
challenge 172 Б вместо 10 Б): драйвер ждёт ~1,4 с и возвращает ERROR_GEN_FAILURE
→ на экране «Внутренняя ошибка микропрограммы 00000». Три одинаковых цикла за 15 с.

Обработчик AUTH приложения 2.22.3 (0x0800722C):
    ldrh [packet+1] == 0xAC  — проверка длины challenge          ✓ ПК шлёт 0xAC
    svc 7  (серийный)        → [sp+0x58]
    svc 8  ×2 (ключи из крипто-блоба бутлоадера 0x08000184) → [sp+0x5C],[sp+0x60]
    bl 0x0800C15C            — крипто-ядро (обфусцировано, читает UID через пул 0x0800C520)
    cbz r0 → построение и отправка ответа; иначе статус 6

ПАТЧ: вызов крипто-ядра @0x0800728E заменяется на «movs r0,#0; nop» (4 Б) —
обработчик сразу идёт по ветке «успех» и ОТПРАВЛЯЕТ ответ ПК (тело будет
нулевым/мусорным — ПК отвергнет его проверкой, но сам факт ответа решает всё).

Интерпретация результата:
  - ПК получил ЛЮБОЙ ответ на AUTH (ошибка ≠ 00000) → главный цикл, диспетчер
    и отправка приложения живут; зависание — ВНУТРИ крипто-ядра 0x0800C15C
    (дальше копать его: входы донорские, обфускация/тактирование/UID-пул);
  - снова тишина → 00000 → приложение умирает ДО диспетчера (init):
    следующий шаг — MODE1 (поколение платы), затем разбор 240 init-запросов
    и данных 0x8B (68 Б, посылаются только новому поколению бутлоадера).

Строится на базе SM2Pro_full_flash_2.22.3_patched_v2.bin (9-словный UID-патч
клона + исправленные EEPROM-слоты 3–8 и загрузочная запись 2.22.3).
Ровно 4 байта отличаются от базы (проверено побайтовым сравнением).
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# Где искать базовый образ patched_v2: рядом, в дереве репозитория, на исходном стенде
CANDIDATES = [
    os.path.join(HERE, "SM2Pro_full_flash_2.22.3_patched_v2.bin"),
    os.path.join(HERE, "..", "..", "firmware", "SM2Pro_full_flash_2.22.3_patched_v2.bin"),
    "/home/z/my-project/fw_analysis/OUTPUT/SM2Pro_full_flash_2.22.3_patched_v2.bin",
]

# 0x0800728E: bl 0x0800C15C (04 F0 65 FF) -> movs r0,#0 (00 20); nop (00 BF)
PATCH_OFF = 0x728E
PATCH_OLD = bytes.fromhex("04f065ff")
PATCH_NEW = bytes.fromhex("002000bf")

OUT_LOCAL = os.path.join(HERE, "SM2Pro_full_flash_2.22.3_AUTH_BYPASS.bin")
OUT_REPO = os.path.normpath(os.path.join(HERE, "..", "..", "firmware",
                                         "SM2Pro_full_flash_2.22.3_AUTH_BYPASS.bin"))

# Эталон собранного образа (см. README, раздел «Хэши образов»)
EXPECTED_MD5 = "d376d61db449d9df4d2a95e3a1bde49d"
EXPECTED_SHA256 = "66333994945ea5943aedfafc0475970db6c914cdd2892f6100198c4245fcc962"


def find_src():
    for c in CANDIDATES:
        if os.path.isfile(c):
            return os.path.normpath(c)
    sys.exit("!! базовый образ SM2Pro_full_flash_2.22.3_patched_v2.bin не найден:\n  " +
             "\n  ".join(CANDIDATES))


def main():
    src = find_src()
    img = bytearray(open(src, "rb").read())
    assert len(img) == 0x40000, f"неожиданный размер образца: {len(img):#x}"

    cur = bytes(img[PATCH_OFF:PATCH_OFF + 4])
    if cur != PATCH_OLD:
        sys.exit(f"!! по смещению 0x{PATCH_OFF:X} ожидалось {PATCH_OLD.hex()}, "
                 f"найдено {cur.hex()} — база не является patched_v2?")
    img[PATCH_OFF:PATCH_OFF + 4] = PATCH_NEW
    print(f"0x{0x08000000 + PATCH_OFF:08X}: {PATCH_OLD.hex(' ')} -> {PATCH_NEW.hex(' ')}"
          f"   bl 0x0800C15C -> movs r0,#0; nop  (AUTH: ответ без крипто-ядра)")

    out = OUT_REPO if os.path.isdir(os.path.dirname(OUT_REPO)) else OUT_LOCAL
    with open(out, "wb") as f:
        f.write(img)

    md5 = hashlib.md5(img).hexdigest()
    sha = hashlib.sha256(img).hexdigest()
    print(f"Записано: {out}")
    print(f"  MD5:    {md5}")
    print(f"  SHA256: {sha}")
    if md5 == EXPECTED_MD5 and sha == EXPECTED_SHA256:
        print("  Совпадает с эталоном — сборка воспроизводима.")
    else:
        print("  !! НЕ СОВПАДАЕТ с эталоном — проверить базу!")
        sys.exit(1)


if __name__ == "__main__":
    main()
