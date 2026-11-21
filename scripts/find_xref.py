# -*- coding: utf-8 -*-
# Ghidra: найти все ссылки на адрес 0x0800E958 и дизассемблировать содержимое
# @category Analysis
from ghidra.program.model.address import AddressSet

fm = currentProgram.getFunctionManager()
af = currentProgram.getAddressFactory()
target = toAddr(long("0800E958", 16))
print("=== Refs to 0x0800E958 ===")
rm = currentProgram.getReferenceManager()
refs = rm.getReferencesTo(target)
for r in refs:
    print("  from %s : %s" % (r.getFromAddress(), r.getReferenceType()))

# Также поиск ссылок на значения 0x080028E8 / 0x1FFFF7E8 как литералы
listing = currentProgram.getListing()
for addr_str in ["0800E958"]:
    t = toAddr(long(addr_str, 16))
    data = listing.getDataAt(t)
    if data is not None:
        print("Data at %s: %s = %s" % (t, data.getDataType(), data.getValue()))

# Кто ссылается на диапазон пула 0x0800E94C-0x0800E964
print("=== Refs to pool area ===")
for a in range(0x0800E940, 0x0800E968, 2):
    t = toAddr(a)
    for r in rm.getReferencesTo(t):
        print("  to 0x%X from %s" % (a, r.getFromAddress()))
