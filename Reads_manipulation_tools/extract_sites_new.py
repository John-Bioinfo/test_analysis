from collections import Counter
from collections import defaultdict
import numpy as np
import argparse
import os, re
import sys

patNum = re.compile("(\d+)[M|D|I]")
patSym = re.compile("([M|D|I])")
patLS = re.compile("^(\d+)S(.*)")
patRS = re.compile("(.*?)(\d+)S$")

datf = sys.argv[1]

def recoverSEQ(seq, matchNum, matchLabel): 
    outSeq = ""
    start = 0
    for num, i in enumerate(matchNum):
        
        if matchLabel[num] == "M":
            outSeq += seq[start: start+int(i)]
            start += int(i)
        elif matchLabel[num] == "I":
            start += int(i)
            
        elif matchLabel[num] == "D":
            outSeq += "N" * int(i)
    return outSeq

def parseDAT(fileIn, Pos, mut_base, distance= 120):

    reads_d = {}
    mut_reads = []
    samHandle = open(fileIn, "r")
    outHaplotypeStr = defaultdict(dict) 

    n = 0
    for line in samHandle:
        if line.startswith("@"):
            continue
        else:
            LineS = line.strip().split("\t")

            readsID = LineS[0]

            readsSeq = LineS[9]

            chrN = LineS[2]
            pos  = LineS[3]
            CIGAR = LineS[5]

            basePos = int(pos)-1
            if patLS.match(CIGAR) or patRS.match(CIGAR):
                if patLS.match(CIGAR) and patRS.match(CIGAR):
                    Lgroup = patLS.match(CIGAR).group(1)
                    Rgroup = patRS.match(CIGAR).group(2)
                    NewCIGAR_info = CIGAR.replace(Lgroup+"S","").replace(Rgroup+"S","")
                    N1_searchAll = patNum.findall(NewCIGAR_info)
                    P1_searchAll = patSym.findall(NewCIGAR_info)
            
                    #print(readsID, chrN, pos, P1_searchAll, N1_searchAll, NewCIGAR_info, Lgroup, Rgroup)
                    newSeq = readsSeq[int(Lgroup):-int(Rgroup)]

                    consensusSeq = recoverSEQ(newSeq, N1_searchAll, P1_searchAll)
                    #print(consensusSeq)
                elif patLS.match(CIGAR):
                    Lgroup = patLS.match(CIGAR).group(1)
                    NewCIGAR_info = CIGAR.replace(Lgroup+"S","")
                
                    N1_searchAll = patNum.findall(NewCIGAR_info)
                    P1_searchAll = patSym.findall(NewCIGAR_info)
            
                    #print(readsID, chrN, pos, P1_searchAll, N1_searchAll, NewCIGAR_info, Lgroup)
                    newSeq = readsSeq[int(Lgroup):]
                    consensusSeq = recoverSEQ(newSeq, N1_searchAll, P1_searchAll)
                    #print(consensusSeq)
                elif patRS.match(CIGAR):      
                    Rgroup = patRS.match(CIGAR).group(2)
                    NewCIGAR_info = CIGAR.replace(Rgroup+"S","")
                    N1_searchAll = patNum.findall(NewCIGAR_info)
                    P1_searchAll = patSym.findall(NewCIGAR_info)
            
                    #print(readsID, chrN, pos, P1_searchAll, N1_searchAll, NewCIGAR_info, Rgroup)
                    newSeq = readsSeq[:-int(Rgroup)]
                    consensusSeq = recoverSEQ(newSeq, N1_searchAll, P1_searchAll)
                    #print(consensusSeq)
            else:
                N1_searchAll = patNum.findall(CIGAR)
                P1_searchAll = patSym.findall(CIGAR)
            
                #print(readsID, chrN, pos, P1_searchAll, N1_searchAll, CIGAR)

                consensusSeq = recoverSEQ(readsSeq, N1_searchAll, P1_searchAll)
            posBase = {}

            seq_L = len(consensusSeq)
            for i in range(seq_L):
                s = int(pos) + i
                ##  posL.append(chrN +":" + str(s))

                if chrN +":" + str(s) == Pos:
                    posBase[readsID] = consensusSeq[i]
                    if i >= 120:
                        l_flanking_seq = consensusSeq[i-distance:i]
                    else:
                        l_flanking_seq = (120-i) * "-" + consensusSeq[:i]
                    if seq_L > i+distance:
                        r_flanking_seq = consensusSeq[i : i+distance]
                    else:
                        r_flanking_seq = consensusSeq[i :] + (i+distance -seq_L)*"-"
                    
                    reads_d[readsID] = l_flanking_seq + r_flanking_seq
                    break
            
            for i in posBase:
                if posBase[i] == mut_base:
                    mut_reads.append(i)
    samHandle.close()
    return mut_reads, reads_d

input_Pos = 'chr5:67591007'
distance = 120

chrN      = input_Pos.split(':')[0]
basep     = int(input_Pos.split(':')[1])

totChr = open('/data2/test/zyqiao_test/mut_compare/p_bam/hg19_fa/' + chrN + '.fa', 'r').read().replace(">" + chrN, '').replace('\n', '')

ref_sequence = totChr[basep-distance-1: basep+distance -1 ]

#ref_sequence = "CTGGGAAACCATAGTGAAACTTTTCATAAACTTTGGGGACCGTTCCTGATGTACCCAGATAATAACAAATACGTTTCTTTTGCCTGCAGGATTATGCATAATTATGATAAGTTGAAGTCTCGAATCAGTGAAATTATTGACAGTAGAAGAAGATTGGAAGAAGACTTGAAGAAGCAGGCAGCTGAGTATCGAGAAATTGACAAACGTATGAACAGCATTAAACCAGACCTTATCCAGCTG"
out_L, out_all_reads = parseDAT(datf, input_Pos, "T")

outF = open("test_con_mut_reads.txt", 'w')
outF.write(ref_sequence + '\n')

for i in out_all_reads:
    if i in out_L:
        mut_seq = out_all_reads[i]
        for n,j in enumerate(mut_seq):
            if j != ref_sequence[n]:
                outF.write('*')
            else:
                outF.write(j)
        outF.write('\n')
        #print(out_all_reads[i])
outF.close()


