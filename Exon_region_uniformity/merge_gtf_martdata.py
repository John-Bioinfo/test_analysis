#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re

gtf = 'hg19_gencode_basic.gtf'
martfile = 'mart_export.txt'

tranC_pat = re.compile("transcript_id \"(.*?)\..*?\";")

martInfo_D = {}
martDataH = open(martfile, 'r')
for line in martDataH:
    if line.startswith('Gene stable ID'):
        continue
    else:
        mx = line.rstrip().split('\t')
        martInfo_D[mx[1]] = mx[0] + '\t' + '\t'.join(mx[2:])
        
martDataH.close()

gtfH = open(gtf,  'r')
for line in gtfH:
    x = line.rstrip().split('\t')
    match = re.search(tranC_pat, x[8])
    if match:
        transcriptID = match.group(1)
        if transcriptID in martInfo_D:
            print(line.rstrip() + '\t' + martInfo_D[transcriptID])
        else:
            print(line.rstrip() + '\tTranscript Not Found' + '\t-'*5 )
    else:
        print("Not match in " + x[0] +"!")

gtfH.close()
