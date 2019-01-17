#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys

exonsFile  =  sys.argv[1]
depFile    =  sys.argv[2]

dp = {}

p_handle   =  open(   exonsFile,  'r'  )
for line in p_handle:
    x = line.rstrip().split('\t')
    start = int(x[3])
    end   = int(x[4])

    for i in range(start, end + 1):
        dp[x[0]+':' + str(i)] = 1

p_handle.close()

depth = {}


d_handle = open(depFile,  'r')
for line in d_handle:
    if line.startswith('chrom'):
        continue
    else:
        x = line.rstrip().split('\t')
        p = x[0] + ':' + x[1]
        if p in dp:
            # print(line.rstrip())
            depth[p] = int(x[3])

d_handle.close()

pnum = len(dp)
totdep = sum(list(depth.values()))
aveDep = totdep/pnum * 1.0
print('Average depth is {0}'.format(aveDep))

aboveNum = 0
for i in depth:
    if depth[i] > 0.2 * aveDep:
        aboveNum += 1
        
print('Uniformity20 is {0:.4f}'.format(aboveNum * 100.0 / pnum))

