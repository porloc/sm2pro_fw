# coding: utf-8
# Ghidra: найти диспетчера таблицы команд и все ссылки на таблицу/функцию 0x0800E764
# @category Analysis
fm = currentProgram.getFunctionManager()
rm = currentProgram.getReferenceManager()
listing = currentProgram.getListing()

print("=== 1. Ссылки НА функцию 0x0800E764 ===")
t = toAddr(long("0800E764", 16))
for r in rm.getReferencesTo(t):
    print("  from %s (%s)" % (r.getFromAddress(), r.getReferenceType()))

print("=== 2. Ссылки НА ячейку таблицы 0x0800F240 (запись {0x0800E765, 0x16}) ===")
t = toAddr(long("0800F240", 16))
for r in rm.getReferencesTo(t):
    print("  from %s (%s)" % (r.getFromAddress(), r.getReferenceType()))

print("=== 3. Ссылки на диапазон таблицы 0x0800F17C..0x0800F2C0 ===")
found = False
for a in range(0x0800F17C, 0x0800F2C4, 4):
    t = toAddr(long("%08X" % a, 16))
    for r in rm.getReferencesTo(t):
        print("  to 0x%X from %s (%s)" % (a, r.getFromAddress(), r.getReferenceType()))
        found = True
if not found:
    print("  (нет)")

print("=== 4. Функции, содержащие ссылки на область 0x0800F000-0x0800F2E0 ===")
seen = set()
for a in range(0x0800EF00, 0x0800F2E8, 4):
    t = toAddr(long("%08X" % a, 16))
    for r in rm.getReferencesTo(t):
        f = fm.getFunctionContaining(r.getFromAddress())
        fn = "%s @ %s" % (f.getName(), f.getEntryPoint()) if f else "???"
        if fn not in seen:
            seen.add(fn)
            print("  %s -> 0x%X" % (fn, a))

print("=== 5. Что за данные на 0x0800F2C4 (init-таблица) ===")
t = toAddr(long("0800F2C4", 16))
for r in rm.getReferencesTo(t):
    print("  from %s (%s)" % (r.getFromAddress(), r.getReferenceType()))

print("=== 6. Дизассемблирование вершины main/диспетчера ===")
# Ищем функцию, которая читает [rX,#4] (код команды) и вызывает [rX] (обработчик)
# Выведем все функции, где есть blx reg рядом с ldr [.., #4] + cmp
from ghidra.program.model.pcode import PcodeOp
ops = {}
for f in fm.getFunctions(True):
    body = f.getBody()
    ins_iter = listing.getInstructions(body, True)
    has_blx = False
    for ins in ins_iter:
        mn = ins.getMnemonicString()
        if mn == "BLX" or mn == "blx":
            has_blx = True
            break
    if has_blx:
        # проверим наличие cmp перед blx в пределах функции
        txt = []
        ins_iter = listing.getInstructions(body, True)
        prev = []
        for ins in ins_iter:
            mn = ins.getMnemonicString()
            if mn.lower() == "blx":
                for p in prev[-8:]:
                    if p[1].lower() in ("cmp","ldr") or "ldr" in p[1].lower():
                        pass
                # печатаем контекст
                for p in prev[-6:]:
                    txt.append("    0x%s: %s %s" % (p[0], p[1], p[2]))
                txt.append("    0x%s: %s %s   <<< BLX" % (ins.getAddress(), ins.getMnemonicString(), str(ins)))
            prev.append((str(ins.getAddress()), ins.getMnemonicString(), str(ins)))
        if txt:
            print("  Функция %s @ %s:" % (f.getName(), f.getEntryPoint()))
            for line in txt[:40]:
                print(line)
            print()
