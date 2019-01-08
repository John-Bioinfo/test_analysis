#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import sys

depG   = [1, 5, 10, 50, 100 , 200]
depthD = dict(zip(depG, [ 0 ] * len(depG) ))

inputDEP = sys.argv[1]

depHandle = open(  inputDEP  ,  'r'  )
for line in depHandle:
    #x = line.strip().split('\t')
    x = line.strip().split()
    d = int(x[2])
    
    tmp_a =  [d//i for i in depG]
    ki    = tmp_a.index(min([i for i in tmp_a if i > 0 ]))
    depthD[depG[ki]] += 1

depHandle.close()

for i in depthD:
    print(i, depthD[i])
                    

#print("{0}\t{1}".format(matchStr, spLine[7]))
