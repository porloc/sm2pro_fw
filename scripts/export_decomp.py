# -*- coding: utf-8 -*-
# Ghidra Jython script: export decompiled C of all functions in range
# args: startAddr endAddr outFile
# @category Analysis
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

args = getScriptArgs()
startAddr = toAddr(long(args[0], 16))
endAddr   = toAddr(long(args[1], 16))
outFile   = args[2]

decomp = DecompInterface()
decomp.openProgram(currentProgram)
monitor = ConsoleTaskMonitor()

fm = currentProgram.getFunctionManager()
funcs = fm.getFunctions(startAddr, True)
out = open(outFile, "w")
count = 0
for f in funcs:
    ea = f.getEntryPoint()
    if ea.getOffset() > endAddr.getOffset():
        break
    res = decomp.decompileFunction(f, 120, monitor)
    callers = ",".join(str(x) for x in f.getCallingFunctions(None))
    if res.decompileCompleted():
        out.write("/* ===== %s @ %s | callers: %s ===== */\n" % (f.getName(), ea, callers))
        out.write(res.getDecompiledFunction().getC())
        out.write("\n\n")
        count += 1
    else:
        out.write("/* FAILED decompile %s @ %s */\n\n" % (f.getName(), ea))
out.close()
print("EXPORTED %d functions to %s" % (count, outFile))
