#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys

file1 = sys.argv[1]     ## /data/project_info/bed_file/620-panel/V3/620gene_V3.intervals
file2 = sys.argv[2]     ## /data/project_info/bed_file/620-panel/V2/620gene_V2.intervals


p1 = open(file1,  'r')
p2 = open(file2,  'r')


d1 = {}
d2 = {}

for line in p1:
    if not line.startswith('@'):
        x = line.rstrip().split('\t')
        start = int(x[1])
        end   = int(x[2])

        for i in range(start, end + 1):
            d1[x[0]+":"+str(i)] = "\t".join(x[:3])
p1.close()


for line in p2:
    if not line.startswith('@'):
        x = line.rstrip().split('\t')
        start = int(x[1])
        end   = int(x[2])

        for i in range(start, end + 1):
            d2[x[0]+":"+str(i)] = "\t".join(x[:3])
p2.close()

s1 = set(d1.keys())
s2 = set(d2.keys())

S1only = s1 - s2
S2only = s2 - s1

andS12 = s1 & s2

print(len(S1only))
print(len(S2only))

print(len(andS12))

outS = set()
for i in S1only:
    outS.add(d1[i])

for p in sorted(list(outS)):
    print(p)


