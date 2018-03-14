#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from typing import List
from typing import Dict
from typing import Tuple
from collections import defaultdict
from glob import glob

def getTPM(countfiles: List[str], lengthF: str, readsLength :float = 100.0) -> Tuple:


    Tlist = []
    dsamples = defaultdict(list)

    Olength = open(lengthF, "r")

    lengthD = {}
    for line in Olength:
        if line.startswith("geneName"):
            continue
        else:
            xg = line.strip().split()
            lengthD[xg[0]] = int(xg[1])

    Olength.close()

    for i in countfiles:
        ac = open(i , "r")
        TA = 0
        for line in ac:
            g_line = line.strip().split("\t")

            if g_line[0] not in [ "__no_feature", "__ambiguous", "__too_low_aQual", "__not_aligned", "__alignment_not_unique"]:
                geneLen = lengthD[g_line[0]]
                TA += int(g_line[1]) * readsLength / geneLen

        SampleTInfo = "{0}-{1:.3f}".format(i, TA)
        Tlist.append(SampleTInfo)
        ac.close()
#    return Tlist

    for a in Tlist:
        sa = a.split("-")
        countFile = sa[0]
        T = float(sa[1])

        bc = open(countFile, "r")

        for line in bc:
            b_line = line.strip().split("\t")
            if b_line[0] not in [ "__no_feature", "__ambiguous", "__too_low_aQual", "__not_aligned", "__alignment_not_unique"]:
                geneLen = lengthD[b_line[0]]
                count = int(b_line[1])
                TPM = count * readsLength * 10 ** 6 / (T * geneLen)
  
                Tvalues = "{0}:{1}:{2:.3f}".format(b_line[0], count, TPM)
                dsamples[countFile].append(Tvalues)

        bc.close()

    return (Tlist, dsamples)
cfiles = glob("*counts_out.txt")

  
outT, outS = getTPM(cfiles, "testHG19_geneLen.txt")

print(outT)

samples = list(outS.keys())
geneNames =[i.split(":")[0] for i in outS[samples[0]]]

outF = open("outGene_TPM.xls", "w")

outF.write("gene_name")

for s in samples:
    outF.write("\t{0}\t{1}".format(s, s+"_TPM"))

outF.write("\n")

for num,i in enumerate(geneNames):
    
    #print(i)
    outF.write(i)
    for j in samples:

        vs = outS[j][num].split(":")[1:]
        outF.write("\t{0}".format("\t".join(vs)))

    outF.write("\n")

outF.close()
