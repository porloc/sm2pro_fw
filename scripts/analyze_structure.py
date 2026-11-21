#!/usr/bin/env python3
"""Анализ структуры дампа прошивки STM32F105VCT6 (SM2 / SM2Pro)."""
import sys, struct

BIN = "/home/z/my-project/fw_analysis/SM2_2.21.32_A111788_STM32F105VCT6.bin"
FLASH_BASE = 0x08000000

data = open(BIN, "rb").read()
print(f"Размер файла: {len(data)} байт (0x{len(data):X}) = {len(data)/1024:.1f} KB")
print()

# ---- 1. Таблица векторов (первые 2 слова: SP, Reset) ----
sp, reset = struct.unpack_from("<II", data, 0)
print(f"Начальный SP : 0x{sp:08X}  (RAM: 0x20000000..0x20010000, {((sp-0x20000000)//1024)}KB в RAM)")
print(f"Reset handler: 0x{reset:08X}")
print()

# ---- 2. Полная таблица векторов ----
print("Таблица векторов (первые 16):")
names = ["SP", "Reset", "NMI", "HardFault", "MemManage", "BusFault", "UsageFault", "R1", "R2", "R3", "R4", "SVCall", "DebugMon", "R", "PendSV", "SysTick"]
for i in range(16):
    v = struct.unpack_from("<I", data, i*4)[0]
    print(f"  [{i:2d}] {names[i]:<10} = 0x{v:08X}")

# Векторы прерываний STM32F105 (offset 16 = WWDG, дальше периферия)
print()
print("IRQ вектора (16-67):")
irq_names = ["WWDG","PVD","TAMPER","RTC","FLASH","RCC","EXTI0","EXTI1","EXTI2","EXTI3","EXTI4",
             "DMA1_CH1","DMA1_CH2","DMA1_CH3","DMA1_CH4","DMA1_CH5","DMA1_CH6","DMA1_CH7",
             "ADC1_2","USB_HP_CAN_TX","USB_LP_CAN_RX0","CAN_RX1","CAN_SCE","EXTI9_5",
             "TIM1_BRK","TIM1_UP","TIM1_TRG_COM","TIM1_CC","TIM2","TIM3","TIM4","TIM5",
             "SPI1","SPI2","USART1","USART2","USART3","EXTI15_10","RTCAlarm","OTG_FS_WKUP",
             "R","R","R","R","TIM6","TIM7","DMA2_CH1..5","ETH","ETH_WKUP","CAN2_TX","CAN2_RX0",
             "CAN2_RX1","CAN2_SCE","OTG_FS"]
for i in range(len(irq_names)):
    off = (16+i)*4
    if off+4 > len(data): break
    v = struct.unpack_from("<I", data, off)[0]
    valid = 0x08000001 <= v <= 0x0803FFFF if v else False
    print(f"  IRQ{i:2d} {irq_names[i]:<14} = 0x{v:08X} {'OK' if valid else ('--' if v==0 else '???')}")

# ---- 3. Поиск второй таблицы векторов (начало приложения) ----
print()
print("Поиск кандидатов на начало приложения (вторая таблица векторов):")
for off in range(0x200, len(data)-8, 4):
    w0, w1 = struct.unpack_from("<II", data, off)
    # SP приложения должен быть в RAM (0x2000xxxx), reset - во flash с Thumb-битом
    if 0x20000000 <= w0 <= 0x20010000 and (w0 & 3) == 0:
        if 0x08000001 <= w1 <= FLASH_BASE + len(data) and (w1 & 1) == 1:
            # и несколько последующих векторов тоже валидны
            ok = True
            for k in range(2, 10):
                v = struct.unpack_from("<I", data, off+4*k)[0]
                if not (0x08000001 <= v <= FLASH_BASE + len(data)):
                    ok = False; break
            if ok:
                print(f"  offset 0x{off:06X} (flash 0x{FLASH_BASE+off:08X}): SP=0x{w0:08X}, Reset=0x{w1:08X}")

# ---- 4. Карта заполненности флеша (по страницам 2КБ) ----
print()
print("Карта заполненности (X = данные, . = 0xFF):")
page = 2048
for i in range(0, len(data), page):
    chunk = data[i:i+page]
    if all(b == 0xFF for b in chunk):
        c = "."
    elif all(b == 0x00 for b in chunk):
        c = "0"
    else:
        c = "X"
    if i % (page*32) == 0:
        print()
        print(f"  0x{FLASH_BASE+i:06X}: ", end="")
    print(c, end="")
print()
print()

# ---- 5. Первые 0xFF-регионы (граница конца полезного кода) ----
first_ff = None
for i in range(len(data)-1, 0, -1):
    if data[i] != 0xFF:
        first_ff = i+1
        break
print(f"Последний непустой байт: 0x{first_ff:06X} (offset), flash 0x{FLASH_BASE+first_ff:08X}")
print(f"Заполнено: {first_ff/1024:.1f} KB из {len(data)/1024:.1f} KB")

# ---- 6. Строки в первых 16КБ (бутлоадер) ----
print()
print("ASCII строки (>=5 симв) в первых 32КБ:")
import re
for m in re.finditer(rb"[\x20-\x7e]{5,}", data[:32768]):
    print(f"  0x{m.start():06X}: {m.group().decode('ascii')!r}")
