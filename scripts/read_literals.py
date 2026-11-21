#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Чтение литеральных пулов (DAT_ адреса) бутлоадера."""
import struct

BIN = "/home/z/my-project/fw_analysis/SM2_2.21.32_A111788_STM32F105VCT6.bin"
FLASH_BASE = 0x08000000
data = open(BIN, "rb").read()

def word(flash_addr):
    off = flash_addr - FLASH_BASE
    return struct.unpack_from("<I", data, off)[0]

def half(flash_addr):
    off = flash_addr - FLASH_BASE
    return struct.unpack_from("<H", data, off)[0]

def show(name, addr, kind="word"):
    if kind == "word":
        v = word(addr)
        print(f"  {name} @ 0x{addr:08X} = 0x{v:08X}")
    else:
        v = half(addr)
        print(f"  {name} @ 0x{addr:08X} = 0x{v:04X}")
    return v

print("=== Литералы протокола обновления ===")
a_upd = show("DAT_08001180 (update ctx)", 0x08001180)
v184 = show("DAT_08001184 (flash write start)", 0x08001184)
v188 = show("DAT_08001188", 0x08001188)
k1  = show("DAT_0800118c (KEY1)", 0x0800118c)
k2  = show("DAT_08001190 (KEY2)", 0x08001190)
v194 = show("DAT_08001194 (offset limit)", 0x08001194)
app_ptr = show("DAT_08001198 (app vector ptr)", 0x08001198)
print()
print("=== Литералы state machine ===")
show("DAT_080013f8 (state struct)", 0x080013f8)
show("DAT_080013fc (app vtable)", 0x080013fc)
show("DAT_08001400 (LED/port)", 0x08001400)
show("DAT_08001404 (param for 0x08001986)", 0x08001404)
print()
print("=== Литералы EEPROM ===")
e1 = show("DAT_08001bd8 (page1)", 0x08001bd8)
e2 = show("DAT_08001bdc (page2)", 0x08001bdc)
print()
print("=== Литералы UART/USB ===")
show("DAT_08001ef0 (uart ctx)", 0x08001ef0)
show("DAT_08001ef4", 0x08001ef4)
show("DAT_08001ef8 (UART CR?)", 0x08001ef8)
show("DAT_08001efc (USB regs?)", 0x08001efc)
show("DAT_08001f00", 0x08001f00)
show("DAT_08001f04", 0x08001f04)
show("DAT_08001f08 (UART base?)", 0x08001f08)
show("DAT_08001f10 (clk)", 0x08001f10)
show("DAT_08001f14 (BRR?)", 0x08001f14)
show("DAT_08001f18", 0x08001f18)
show("DAT_08001f1c", 0x08001f1c)
show("DAT_08001f20", 0x08001f20)
print()
print("=== Прочее ===")
show("DAT_08002388 (iface state)", 0x08002388)
show("DAT_0800238c", 0x0800238c)

print()
print("=== По указателю DAT_08001198 (значение = вектор приложения?) ===")
if 0x08000000 <= app_ptr < 0x08040000:
    sp, rst = word(app_ptr), word(app_ptr+4)
    print(f"  app @ 0x{app_ptr:08X}: SP=0x{sp:08X}, Reset=0x{rst:08X}")

print()
print("=== Крипто-блоб 0x08000184 (128 байт) ===")
import binascii
blob = data[0x184:0x204]
for i in range(0, 128, 16):
    print("  0x%08X: %s" % (0x08000184+i, " ".join(f"{b:02X}" for b in blob[i:i+16])))
print()
print("=== Серийник 0x08000180 ===")
print(f"  0x08000180 = 0x{word(0x08000180):08X} = '{word(0x08000180):07X}'")
