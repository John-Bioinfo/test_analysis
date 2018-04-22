#!/usr/bin/env python
# -*- coding: UTF-8 -*-


__author__      = "Zongyun Qiao"
__copyright__   = "Copyright 2018, Biotech"
__credits__     = [
    "Zongyun Qiao"]  # remember to add yourself
__license__     = "GPL"
__version__     = "0.1-dev, 20180422"
__maintainer__  = "Zongyun Qiao"
__email__       = "gulile@yeah.net"


import sys

inputSam = sys.argv[1]

#def revComp(seq, qua):
#    x = ""
#    for i in seq:
#        x   += dbase[i]
#    rx   = x[::-1]
#    rq = qua[::-1]
#    return rx, rq


dbase = {"A":"T", "T":"A", "G":"C", "C":"G"}
def revComp(seq):
    x = ""
    for i in seq:
        x   += dbase[i]
    rx   = x[::-1]

    return rx

d_barcode = {}

handleA = open(inputSam, "r")

totNum = 0

for line in handleA:
    x = line.strip().split("\t")
    flag = int(x[1])
    #print(flag)
    if flag == 0:
        totNum += 1
        barcodex = x[9][0:12] 
        #print(barcodex)
        d_barcode[barcodex] = d_barcode.get(barcodex, 0) +1
    elif flag == 16:
        totNum += 1
        revSeq = revComp(x[9])
        barcodex = revSeq[0:12]
        #print(barcodex)
        d_barcode[barcodex] = d_barcode.get(barcodex, 0) +1
handleA.close()

sortBarCo = sorted(d_barcode.items(), key = lambda x: x[1], reverse=True)


# python A_prog_for_readsFilter.py TestInput_81.sam

fileOut = open("barcodes_res.txt", "w")
#for i in d_barcode:
for k, num in sortBarCo:
    #print(i, d_barcode[i])
    #print(k, "{0:.8f}".format(num * 1.0/ totNum))
    print("{0}\t{1:.8f}".format(k, num * 1.0/ totNum), file=fileOut)
fileOut.close()

print(len(sortBarCo))
    
