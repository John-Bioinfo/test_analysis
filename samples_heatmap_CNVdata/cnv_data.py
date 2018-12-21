#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys

def filterCNV_Seg(annofile, r):
    d = {}
    filehandle = open(annofile, "r")
    for line in filehandle:
        if line.startswith("#Chromosome"):
            continue
        else:
            xline = line.strip().split("\t")
            seg_mean = float(xline[4])
            genename = xline[6]
            #if seg_mean >= r:
            if seg_mean != r:
                #print(seg_mean, genename)
                gx = genename.split(":")[-1]
                #d[gx] = 1
                d[gx] = "-\t"+ xline[4]

    filehandle.close()
    return d
d = filterCNV_Seg("test.select.xls",  1)

for i in d:
    print("{0}\t{1}".format(i, d[i]))
