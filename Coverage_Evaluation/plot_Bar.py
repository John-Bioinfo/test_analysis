#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import sys
import linecache

testDat = np.loadtxt(sys.argv[1], delimiter="\t", usecols=np.arange(1,4), dtype=(float), skiprows=1)
header = linecache.getline(sys.argv[1], 1)
colnames = header.rstrip().split('\t',1)[1].split('\t')

rowN   = len(testDat)
colNum = np.size(testDat, 1)

totalWid = 1.2
x = np.arange(rowN)
width = totalWid / (rowN )
x = x - (totalWid - width) / 2

fig = plt.figure()

for c in range(colNum):
    plt.bar(x + width * c, testDat[:, c],width = width, label=colnames[c])
    
plt.legend()

new_ticks1 = ['>1X', '>5X', '>10X', '>50X', '>100X', '>200X']  
plt.xticks(x+ width, new_ticks1, rotation = 0)

#plt.show()
geneName = sys.argv[1].split('_')[0]
fig.suptitle(geneName,fontsize=18)
fig.savefig(geneName + '_stats' +'_depth.png')
