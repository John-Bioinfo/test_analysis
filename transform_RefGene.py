#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from Bio import SeqIO

inputH = open("/results/qiaozy/annovar/Annovar/humandb/hg19_refGene.txt", "r")


d_geneName = dict()

for line in inputH:
    F = line.strip().split("\t")
    genename = F[12] + F[2]

    s = int(F[4])
    end = int(F[5])
    #print(end-s)
    exonN = F[8]
    #print(exonN)
    if genename not in d_geneName:
        d_geneName[genename] = str(end-s)+";"+exonN+";"+F[1]

    else:
        cv = d_geneName[genename]
        
        vs = cv.split(";")
        vLen = int(vs[0])
        vNum = int(vs[1])

        if end -s >= vLen and int(exonN) > vNum:
            d_geneName[genename] = str(end-s)+";"+str(exonN)+ ";" +F[1]

inputH.close()

IDList = []

outF = open("N_hg19_refGene.txt", "w")
newIn = open("/results/qiaozy/annovar/Annovar/humandb/hg19_refGene.txt", "r")

for line in newIn:
    F = line.strip().split("\t")

    s = int(F[4])
    end = int(F[5])

    exonN = F[8]

    V = d_geneName[F[12]+F[2]].split(";")

    if str(end-s) == V[0] and exonN == V[1] and F[1] == V[2]:
        outF.write(line)
        IDList.append(F[1])

outF.close()
newIn.close()
    

outFa = open("N_hg19_refGeneMrna.fa", "w")

for rec in SeqIO.parse("/results/qiaozy/annovar/Annovar/humandb/hg19_refGeneMrna.fa", "fasta"):
    if rec.id in IDList:
        SeqIO.write(rec, outFa, "fasta")

outFa.close()





