#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys

depG   = [1, 5, 10, 50, 100 , 200]
depthD = dict(zip(depG, [ 0 ] * len(depG) ))

inputDEP = sys.argv[1]
bedF     = sys.argv[2]

BED_handle = open(bedF, 'r')
lines = [i.strip() for i in BED_handle.readlines()]
regions = lines[0].split('\t')[1:3]
BED_handle.close()

length = int(regions[1]) - int(regions[0]) + 1

depHandle = open(  inputDEP  ,  'r'  )
for line in depHandle:
    #x = line.strip().split('\t')
    x = line.strip().split()
    d = int(x[2])
    
    tmp_a =  [d//i for i in depG]
    for n,j in enumerate([i for i in tmp_a if i > 0 ]):
        depthD[depG[n]] += 1

depHandle.close()

header_Name = bedF.replace('.bed', '')
print("Depth_range\t{0}_num\t{1}_percent".format(header_Name, header_Name ))
for i in depG:
    basesN = depthD[i]
    pent   = basesN * 1.0/length
    print(">{0}X\t{1}\t{2:.4f}".format(i, basesN, pent ))
