#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import time
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC
from Bio.Align.Applications import MuscleCommandline

muscle = "/data2/test/zyqiao_test/RNAseq_data/PEAR/muscle3.8.31_i86linux64"
work_dir = "/data2/test/zyqiao_test/RNAseq_data/PEAR/test_Align"

def P_F(f2):
    f_h = open(f2, 'r')
    seqs_Dict = {}
    for Line in f_h:
        if Line[0]==">":
            Name=Line.strip()[1:]
            seqs_Dict[Name] = ""
        else:
            try:
                #try to append with +=
                #assumes Name is a key
                seqs_Dict[Name]+=Line.strip()
            except KeyError:
                seqs_Dict[Name]=Line.strip()
            except UnboundLocalError:
                continue
    f_h.close()
    return seqs_Dict

def AlignStrs(str1, str2):
    sc = ""
    for num, c in enumerate(str1):
        if c == str2[num]:
            sc+=c
        else:
            sc+="-"
    rsc = sc[::-1]
    for n, i in enumerate(sc):
        if i != "-":
            tn = n
            break

    for m, j in enumerate(rsc):
        if j != "-":
            tm = m
            break
    slen = len(sc)

    outAlignC = ""
    for num, i in enumerate(sc):
        if num < n or num > slen - m -1:
        #print ("-", end ="")
            outAlignC += "-"
        elif sc[num] == str1[num]:
        #print (i,   end ="")
            outAlignC += i
        else:
        #print ("*", end ="")
            outAlignC += "*"

    return outAlignC

def alignSEQ(SEQs, s, n):
    outName = []
    for i in SEQs:
        inputName = "TMP_{0:03d}.fa".format(n)
        inFaHandle = open( inputName, "w")
        inFaHandle.write('>' + i + '\n' + SEQs[i] + "\n")

        inFaHandle.write(s)
        inFaHandle.close()
        

        outfile = inputName.replace("TMP_", "aligned_")
        m_cline = MuscleCommandline(muscle, input = inputName, out = work_dir +'/'+ outfile, clw=False)
        m_cline()

        outName.append(outfile)
    return outName

os.chdir(work_dir)
refSeqs = P_F('hlaB_exons.fasta')
geneDict = P_F('tmpHLA-B.fa')

for num,s in enumerate(refSeqs):
    seqFull = '>' + s + '\n' + refSeqs[s]+'\n'
    tmp_names = alignSEQ(geneDict, seqFull, num )
    
