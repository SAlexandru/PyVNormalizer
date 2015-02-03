#! /usr/bin/python
# -*- coding: utf-8 -*-

from lib.pyew.pyew_core import CPyew
import os
import sys
import hashlib

def printData(pyew, path, msg = "default message"):
    buf = pyew.getBuffer()
    
    print "File  :", path
    print "Format :", pyew.format
    print "File Size: ", pyew.maxfilesize
    print "EP offset: ", pyew.ep
    print "Offset: ", pyew.offset
    print "MD5   :", hashlib.md5(buf).hexdigest()
    print "SHA1  :", hashlib.sha1(buf).hexdigest()
    print "SHA256:", hashlib.sha256(buf).hexdigest() 
    print "Found :", msg


if __name__ == '__main__':
    if 2 != len(sys.argv):
        print "Usage: %s filename\n" % (sys.argv[0])
        sys.exit(0)

    fileName = os.path.abspath(sys.argv[1])
    pyew = CPyew(batch = True)
    pyew.codeanalysis = True

    try:
        pyew.loadFile(fileName)
    except:
        _, value, _ = sys.exc_info()
        print "Error in opening file: ", value
    printData(pyew, fileName, "loaded the file!")
    fileName = fileName.replace(".exe", "")
    with open(fileName + "_disasm", "wb") as f:
        for inst in pyew.disasm(pyew.ep, processor = pyew.processor, lines = -1, bsize = pyew.maxfilesize):
            f.write(str(inst) + "\n")

    with open(fileName + "_disasm_bb", 'wb') as f:
        for idx, bb in pyew.basic_blocks.items():
            f.write("---------------- bb: %d ----------------\n" % (idx))
            for inst in bb.instructions:
                f.write(str(inst) + "\n")
            f.write ("---------- Connections: ----------\n")
            for afrom, ato in bb.connections:
                f.write(str(afrom) + ", " + str(ato) + "\n")
            f.write ("---------- inrefs : ----------\n")
            for ir in bb.inrefs:
                f.write(str(type(ir)) + ": " + str(ir) + "\n")
            try:
                f.write ("Name: %s\n" % (bb.name))
            except:
                pass
            f.write("Offset: %d\n" % (bb.offset))
            f.write("----------------------------------------\n")
