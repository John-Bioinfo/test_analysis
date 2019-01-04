#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import gzip
import re
from glob import glob


genes  = ['AR', 'BRCA1', 'BRCA2', 'ATM', 'TP53']

sampleVCFs = glob("./all_cellline_vcf/*vcf.gz")

patt = re.compile('VW=(.*?)\|')
cellline_pat = re.compile('SampleName=(.*?),')

for f in sampleVCFs:
    opVCF = gzip.open(f, "r")
    d_genes = set()
    for line in opVCF:
        if not line.startswith("#"):
            infoLine = line.strip()

            spLine =infoLine.split("\t")
            m1 = re.search(patt, spLine[7])
            if m1 != None:
                matchStr = m1.group(1)
                if matchStr in genes:
                    d_genes.add(matchStr)
                    #print("{0}\t{1}".format(matchStr, spLine[7]))
            
    opVCF.close()
    if len(d_genes) == len(genes):
        print(f)
        VCF_handle = gzip.open(f, "r")
        for line in VCF_handle:
            if line.startswith("##SAMPLE=<ID=TUMOUR,Description=\"Mutant\""):
                infoLine = line.strip()
                cell_Match = re.search(cellline_pat, infoLine)
                
                print("Cell Line: {0}".format(cell_Match.group(1)))
                break
        VCF_handle.close()


