# Захваты обмена (сырые данные)

Все первичные захваты диагностики. Разборы — в `docs/`
(`APIMON_CAPTURE_ANALYSIS.md`, `APIMON2_ANALYSIS.md`, `LOG1_ANALYSIS.md`,
`LOG2_ANALYSIS.md`, `WORKING_22135_ANALYSIS.md`).

## apimon1_22135_working/ — эталон нормы (2.21.35)

Захват API Monitor (x86) рабочей сессии smwin ↔ адаптер на прошивке 2.21.35
(рабочий дамп `firmware/fw_22135.bin`, серийник A71283). 97 вызовов, ~11,7 с.

- `capture.apmx86` — исходный захват (ZIP: definitions + process/0/{info,calls,data})
- `TRANSCRIPT.txt` — построчный протокол всех вызовов с блобами

Ключевое (эталон хендшейка): `0x83 INFO` → ответ {серийный 0x00A71283, версия
0x1096} → `0x88 ARM` → OK → `0x12 AUTH` (challenge 10 Б) → ответ 100 Б с байтами
виртуального UID `52 59` → рабочий цикл опроса статуса. Обновления (0x80–0x82) НЕТ.

## apimon2_2223_patched_v2/ — клон на 2.22.3 (диагноз «00000»)

Захват API Monitor №2: smwin 2.22.3 ↔ клон, прошит
`firmware/SM2Pro_full_flash_2.22.3_patched_v2.bin`. 44 вызова, 15,15 с, 3 цикла.

- `capture2.apmx86` — исходный захват
- `TRANSCRIPT_2.txt` — построчный протокол 44 вызовов

Хронология каждого цикла: INFO (версия 0x1198 — EEPROM-фикс v2 работает) → ARM OK
→ LAUNCH 0x37 {0x1198, 0x210E9A13, 0x1353C} OK → AUTH 0x12 (challenge 172 Б,
новый формат) → **тишина ~1,4 с → ERROR_GEN_FAILURE** → CloseHandle. Это и есть
«Внутренняя ошибка микропрограммы 00000»: запустившееся приложение 2.22.3 молчит
на AUTH. Подробности и лестница проб — `docs/APIMON2_ANALYSIS.md`.

## usbpcap_22135_working/ — USB-трейс рабочего комплекта 2.21.35

- `log_22135.pcapng` — USBPcap-захват (прислан с рабочей машины 2.21.35)
- `report_22135.txt` — отчёт парсера `scripts/parse_usbpcap.py`

## usbpcap_user_00000/ — ранние захваты периода «00000»

- `user_log.pcapng`, `user_report.txt` — третий захват (окно записи не попало
  на обмен; вывод — в `docs/WORKING_22135_ANALYSIS.md`)
- `dev6_bulk.txt`, `dev6_raw.txt` — выжимка по устройству №6 (адаптер) из LOG1
- `flash_logs/` — первые два захвата прошивки v1-образа и их разборы:
  `v1_patched_flash_log`, `v1_patched_flash_log_new` (pcapng), `v1_report.txt`,
  `v1_report_dev6.txt`, `v2_report.txt`, `screenshot_devmgmt` (скриншот диспетчера
  устройств — экземпляр адаптера №3), `vlm_screenshot.json`

Итог по всем USBPcap-захватам: bulk-пакетов адаптера в них нет (окно/фильтры),
протокол полностью покрыт API Monitor — см. `docs/APIMON2_ANALYSIS.md`, раздел
«USBPcap: закрыть вопрос».
