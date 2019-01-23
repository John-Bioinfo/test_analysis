#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from glob import glob
from copy import deepcopy
import pprint

a = glob('*-*.dep')

# usage : python get_Depth_v2.py 1860661-tumor_hlaB_1.dep
depG   = [1, 5, 10, 50, 100 , 200, 500, 1000, 5000, 10000]
GL     = len(depG)
depthD = dict(zip(depG, [ 0 ] * GL ))

def get_D(inputDEP):
    di = deepcopy(depthD)
    
    depHandle = open(  inputDEP  ,  'r'  )
    for line in depHandle:
        x = line.strip().split('\t')
        d = int(x[2])
        if d > 0 :
            tmp_a =  [d//i for i in depG]
            a_L   =  [i for i in tmp_a if i > 0]
            for n, j in enumerate(a_L): 
                di[depG[n]] += 1
    depHandle.close()
    
    return di

outL = []
for depthFile in a:
    do = get_D(depthFile)
    #pprint.pprint(do, width=1)
    outL.append(do)
    
print('{0}\t{1}\t{2}'.format('sample' , 'covLength', '\t'.join([str(i)+'X' for i in depG]) ))
for num, stat in enumerate(outL):
    totalBases  = stat[1]
    #sampleName = '_'.join(a[num].split('_')[:-1])
    sampleName  = a[num].replace('.dep', '')
    print(sampleName + '\t' + str(totalBases), end='')
    for i in depG:
        bn = stat[i]                           ## bases number
        print('\t{0:.2f}'.format( bn*100.0/totalBases ),end='')
    print()



