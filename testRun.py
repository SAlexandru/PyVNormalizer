#! /usr/bin/python
import os
import sys


sys.path.append("pyew")
from pyew_core import CPyew

if __name__ == '__main__':
  if 2 != len(sys.argv):
    print "Usage: testRun filename\n"
    sys.exit(1)

  pyew = CPyew(batch = True)
  pyew.codeanalysis = True

  try:
    pyew.loadFile(os.path.abspath(sys.argv[1]))
  except Exception:
    print "There was an error loading the file"

  print "Will be printing the file disassembeled"
  with open("exe/exec_disassembeled", "wb") as f:
    print "\toffset: ", pyew.ep
    print "\tnumber of lines: ", pyew.lines
    print "\tsize: ", pyew.maxfilesize
    disasm = pyew.disasm(0, processor=pyew.processor, mtype=pyew.type, lines=-1, bsize=pyew.maxfilesize)
    for inst in disasm:
      operands = ''.join(inst.operands)
      operands = operands.replace('[', '')
      operands = operands.replace(']', '')
      f.write(str(inst.mnemonic) + " " + str(operands) + "\n")

