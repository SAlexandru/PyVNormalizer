#! /usr/bin/python
import os
import sys


sys.path.append("pyew")
from pyew_core import CPyew


def printStatistics(cp):
  print "Format: " + cp.format
  print "Lines: " + str(cp.lines)

  cp.showSettings()
  with open("exec", "wb") as f:
    f.write(cp.buf)

  with open("exec_analysis", "wb") as f:
    f.write(str(cp.analyzed))

  with open("exec_flowgraph", "wb") as f:
    f.write(str(type(cp.flowgraphs)))

if __name__ == '__main__':
  if 2 != len(sys.argv):
    print "Usage: testRun filename\n"
    sys.exit(1)

  cp = CPyew(batch = True)
  cp.codeanalysis = True
  cp.deepcodeanalysis = True

  try:
    cp.loadFile(sys.argv[1])
  except Exception:
    print "There was an error loading the file"

  printStatistics(cp)
