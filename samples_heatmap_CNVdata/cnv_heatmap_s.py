#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from collections import defaultdict
import os
import sys

filelist = [  "/WES/test_YHF/BX10057.select.xls",
              "/WES/test_YHF/BX10058.select.xls",
              "/WES/test_YHF/BX10155.select.xls",
              "/WES/test_YHF/BX10161.select.xls",
              "/WES/test_YHF/BX10260.select.xls",
              "/WES/test_YHF/BX10277.select.xls",
              "/WES/test_YHF/BX10526.select.xls",
              "/WES/test_YHF/BX10024.select.xls",
              "/WES/test_YHF/BX10080.select.xls",
              "/WES/test_YHF/BX10070.select.xls",
              "/WES/test_YHF/BX10099.select.xls",
              "/WES/test_YHF/BX10169.select.xls",
              "/WES/test_YHF/BX10183.select.xls",
              "/WES/test_YHF/BX10257.select.xls",
              "/WES/test_YHF/BX10430.cnv.test.xls",
              "/WES/test_YHF/BX10632.select.xls",
              "/WES/test_YHF/BX10636.select.xls",
              "/WES/test_YHF/BX10652.select.xls"
]

             
sampleD = defaultdict(dict)

genes = set()

for i in filelist:
    if os.path.exists(i):
        print("{0} exists!".format(i))

        spX = i.split("/")[-1]
        sampleL = spX.split(".")[0]
        sampleD[sampleL]["Test"] = 1
        fh = open(i, "r" )
        for line in fh:
            if line.startswith("Gene"):
                continue
            else:
                SPLine = line.strip().split("\t")
                sampleD[sampleL][SPLine[0]] = SPLine[2]
                genes.add(SPLine[0])
        fh.close()


outfile = sys.argv[1]

hout = open(outfile, "w")

new_genes = list(genes)

hout.write("sample_name")
for g in new_genes:
    hout.write("\t{0}".format(g))
hout.write("\n")

for i in sampleD.keys():
    hout.write("{0}".format(i))
    for gene in new_genes:
        
        hout.write("\t{0}".format(sampleD[i].get(gene, "1")))
    hout.write("\n")

hout.close()

print(sampleD.keys())
