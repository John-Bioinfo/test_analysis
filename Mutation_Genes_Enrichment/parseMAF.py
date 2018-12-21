#!/usr/bin/env python
# -*- coding:UTF-8 -*-

maffile = "test_outMAF.txt"


omaf = open(  maffile,  "r"  )

setGene = set()

for line in omaf:
    
    if not line.startswith("Chr"):
        x = line.strip().split("\t")
    
        if float(x[11]) >= 0.9:
            setGene.add(x[5])

omaf.close()

print("GeneName")
for i in setGene:
    if ";" in i:
        XI = i.split(";")
        for n  in XI:
            print(n)

    else:
        print(i)
