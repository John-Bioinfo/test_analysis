#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from glob import glob
from collections import defaultdict

resFiles = glob("*_Mutation.xls")

for i in resFiles:
    cellLine = i.split('_')[0]

    d = defaultdict(dict)
    fileH = open( i, 'r' )
    for line in fileH:
        if line.startswith('Gene'):
            continue
        else:
            x = line.strip().split('\t')
            geneCol = x[0].split('_')[0]

            if 'Insertion' in x[8] or 'Deletion' in x[8]:
                d[geneCol]['INDEL'] = d[geneCol].get('INDEL', 0) + 1
            else:
                d[geneCol]['SNV'] = d[geneCol].get('SNV', 0) + 1

    fileH.close()
    
    
    cnvH = open(cellLine+ '_CNV.xls', 'r')
    for line in cnvH:
        if line.startswith('Gene'):
            continue
        else:
            x = line.strip().split('\t')
            geneCol = x[0].split('_')[0]
            d[geneCol]['CNV'] = d[geneCol].get('CNV', 0) + 1
    
    cnvH.close()
    print('{0}_cell_line_gene\tSNV_num\tINDEL_num\tCNV_num'.format(cellLine))
    for gene in d:
        print('{0}\t{1}\t{2}\t{3}'.format(gene, d[gene].get('SNV',0), d[gene].get('INDEL', 0), d[gene].get('CNV', 0)))
