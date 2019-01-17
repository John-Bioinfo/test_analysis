#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from collections import defaultdict
import sys
import re

dbfile    = sys.argv[1]

## dbfile = 'res_data.txt'

geneName  = sys.argv[2]

TMP_1_name = 'tmp_exons_' + geneName +'.txt'
out_TMP_1  = open(TMP_1_name , 'w')

db_handle  = open(dbfile,  'r')
for line in db_handle:
    x = line.rstrip().split('\t')
    if x[2] == 'exon' and x[11] == geneName:
        out_TMP_1.write(line)
out_TMP_1.close()
db_handle.close()

d1 = defaultdict(list)
d_info = defaultdict(list)

tranC_pat = re.compile("transcript_id \"(.*?)\..*?\";")
opTMP_1 = open(  TMP_1_name,  'r')
for line in opTMP_1:
    xt = line.rstrip().split('\t')
    match = re.search(tranC_pat, xt[8])
    tID = match.group(1)
    
    d1[tID].append(int(xt[3]))
    d1[tID].append(int(xt[4]))
    
    d_info[tID].append(line.rstrip())
    
opTMP_1.close()

if len(sys.argv) == 5 :
    for i in d1:
        
        if d1[i][0] >=  int(sys.argv[3]) and d1[i][-1] <= int(sys.argv[4]) :
            transcriptFileName = i + '_' + geneName + '_exons.txt'
            out_Transcript = open(transcriptFileName, 'w')
            
            for info in d_info[i]:

                out_Transcript.write(info + '\n')
            
            out_Transcript.close()
        
else:
    sys.exit('User did not provide gene region. Please refer temp results -- tmp_exons_*.txt')
