#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import time
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC
from Bio.Align.Applications import MuscleCommandline

muscle = "D:/LOHHLA_results/sequence_align/muscle3.8.31_i86win32.exe"
work_dir = "D:/LOHHLA_results/sequence_align/output/"

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

def alignSEQ(SEQs, n):
    inputName = "TMP_raw_{0:03d}.fa".format(n)
    inFaHandle = open( inputName, "w")
    for s in SEQs:
        inFaHandle.write(s+"\n")
    inFaHandle.close()

    outName = inputName.replace("TMP_raw_", "align_")
    m_cline = MuscleCommandline(muscle, input = inputName, out = work_dir + outName, clw=False)
    m_cline()
    return outName

input_S = sys.argv[1]
seqs = P_F(input_S)
seqList = list(seqs.keys())

num = 1
tmpS = []

resFiles = []
os.chdir(work_dir)

print('HLA_Exon_Name\t' + '\t'.join(seqList))
for i in range(len(seqList)):
    if i >= 1:
        print(seqList[i] +  '\t' +  '\t'.join(['0']*i) + '\t1', end = '')
    else:
        print(seqList[i] +  '\t1', end = '')
    
    for j in range(i+1, len(seqList)):
        # print(seqList[i],  seqList[j])
        tmpS.append(">"+seqList[i]+"\n"+seqs[seqList[i]] ) 
        #tmpS.append(">"+seqList[j]+"\n"+seqs[seqList[j]] )
        secondSeq = Seq(seqs[seqList[j]],  IUPAC.unambiguous_dna)
        #tmpS.append(">"+seqList[j]+"-RC\n"+ str(secondSeq.reverse_complement()) )
        tmpS.append(">"+seqList[j]+"\n"+ str(secondSeq) )

        outname = alignSEQ(tmpS, num)
        time.sleep(1.2)
        resSeqs = P_F(outname)
        twoSeqs = list(resSeqs.values())
        alignS  = AlignStrs(twoSeqs[0], twoSeqs[1])
        print("\t{0:.4f}".format( (len(alignS) - alignS.count("*"))/ (1.0* len(alignS)) ),end='')
        
        num += 1
        del tmpS[:]
    print()
#        resFiles.append(outname)

#print(resFiles)
#print(os.getcwd())
#print(os.listdir("./"))

#print("====================================================================")
#for fafile in resFiles:
#    resSeqs = P_F(fafile)
#    twoSeqs = list(resSeqs.values())

#    alignS  = AlignStrs(twoSeqs[0], twoSeqs[1])
#    for s in resSeqs:
#        print(s.ljust(28)+ resSeqs[s] )

#    print("A".ljust(28) + alignS)
#    print("====================================================================")




