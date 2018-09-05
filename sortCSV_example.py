#!/usr/bin/env python
# -*- coding:UTF-8 -*-
from __future__ import with_statement
from __future__ import print_function
from glob import glob
import csv

file1 = "test1_info.xls"
file2 = "test2_info.xls"
file3 = "test3_info.xls"

a = [file1, file2, file3]

l = []

d = {}

for f in a:
    fh = open(f, "r")
    for line in fh:
        if not line.startswith("CHR"):
            z = line.strip().split("\t")
            if z[6] not in l:
                d[z[3]]  =  z[6]
                l.append(z[6])
    fh.close()

for i in a :
    fh = open(i, "r")
    writeF = open("unsorted_" + i, "w")
    for line in fh:
        if not line.startswith("CHR"):
            z = line.strip().split("\t")
            for name in d:
                if z[6] == d[name]:
                    geneN = z[3].split("-")[0]
                    writeF.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\n".format(z[0],z[1], z[2], name, z[4], z[5],z[6], geneN))

        else:
            writeF.write(line.strip()+ "\tGene\n")
    writeF.close()
    fh.close()

unsortFiles = glob("unsorted_*")


for inputN in unsortFiles:
    with open(inputN ) as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter="\t")
        sortedlist = sorted(spamreader, key=lambda row:(int(row['CHR']),int(row['SNP_HOTSPOT'])), reverse=False)

    outF = inputN.replace("unsorted", "Sort")

    #outSortH = open(outF, "w")
    with open(outF, "wb") as outSortH:
        fieldnames = ["CHR","POS_5","POS_3","PROBE","SNP_HOTSPOT","STRAND","SEQ","Gene"]
        writer = csv.DictWriter(outSortH, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for row in sortedlist:
            writer.writerow(row)
    #outSortH.close()
