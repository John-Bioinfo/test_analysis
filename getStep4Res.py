#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os

def FindFile_sample(d_dir, pName):
    if not os.path.isdir(d_dir):
        sys.exit("Directory does not exist. Please check it.")
    T_files = []
    for root, dirs, files in os.walk(d_dir):
        for fr in files:
            # if fr.endswith("Depth_Result.txt"):
            if pName.find("*") != -1:
                name_s = pName.split("*")
                if fr.startswith(name_s[0]) and fr.endswith(name_s[1]):
                    f_path = os.path.join(root, fr)
                    T_files.append(f_path)
            elif fr.endswith(pName):
                f_path = os.path.join(root, fr)
                T_files.append(f_path)
    return T_files

## ref : ../../Test_combination_probes/Nine_months/getStep1res.py

def pickByFreq(d, num):
    List = []
    for i in d:
        if d[i] <= num:
            List.append(i)
    return List

def filterByGC(seqList, GCstd = 54.2):

    outList = []

    for i in seqList:
        seq = i.split("\t")[1]
        Gn = seq.count("G")
        Cn = seq.count("C")
        GCratio = 100.0 * (Gn+Cn)/len(seq)
        if GCratio >= GCstd:
            outList.append(i)

    return outList

fullP = "./"
llFiles = FindFile_sample(fullP, "Step4*Hits.xls" )

AllCandPro = []

for f in llFiles:
    dA = {}

    AllNum = 0
    fh = open(f, "r")
    for line in fh:
        z = line.strip().split("\t")
        dA[z[0]] = dA.get(z[0], 0)+1

        AllNum += 1
    fh.close()

    probeId = dA.keys()
    if len(probeId) < 20 and len(pickByFreq(dA, 5)) < 3:
        probeId = pickByFreq(dA, 15)
    elif len(probeId) < 20 and len(pickByFreq(dA, 5)) >= 3:
        probeId = pickByFreq(dA, 5)

    elif AllNum > 100 and len(probeId) > 20:
        probeId = pickByFreq(dA, 1)
        

    AllSeqs = []
    dirI = os.path.dirname(f)
    baseF = os.path.basename(f)
    sourceF = dirI + "/" + "Test_" + baseF.replace("Step4_blastScore_", "").replace("_filter_ProbeHits.xls","")

    oF = open(sourceF, "r")
    for line in oF:
        xs = line.strip().split("\t")
        if xs[0]+"_F" in probeId:
            AllSeqs.append(xs[0] + "\t" + xs[4])

    oF.close()

    if len(filterByGC(AllSeqs, 48)) < 1:
        AllSeqs = filterByGC(AllSeqs, 30)

    else:
        if len(AllSeqs) > 120:
            AllSeqs = filterByGC(AllSeqs, 48)

        if len(AllSeqs) > 90:
            AllSeqs = filterByGC(AllSeqs, 51.7)

        #if len(AllSeqs) > 50: 
        #    AllSeqs = filterByGC(AllSeqs, 52)

    if len(AllSeqs) < 1:
        print(f)
        print("GC_low")
    else:
        AllCandPro.append(AllSeqs[0:6]) 
        #print("Num is " + str(len(AllSeqs)))

r= [[]]
for x in AllCandPro:
    t=[]
    for y in x:
        for i in r:
            t.append(i+[y])
    r=t

print(len(r))



