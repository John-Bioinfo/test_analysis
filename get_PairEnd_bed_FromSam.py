#!/usr/bin/env python

import sys

def toHex(s):
    ## hv = hex(int(s, 10))
    ts = bin(int(s,10))[2:].zfill(17)
    flags = []

    for n,i in enumerate(ts[::-1]):
        if i=="1":
            s = str(2 ** n)    ## get string for hex converting
            fs = hex(int(s, 10))
            flags.append(fs)

    return flags

inputS = sys.argv[1]

f = open(inputS, "r")

for line in f:
    z = line.rstrip().split("\t")

    flags = toHex(z[1])
    insertSize = int(z[8])
    if insertSize > 0:
        map_end = int(z[3])+ insertSize
        if "0x20" in flags:
            print("{0}\t{1}\t{2}\t-".format(z[2], z[3], map_end))
        
        else:
            print("{0}\t{1}\t{2}\t+".format(z[2], z[3], map_end))
    elif insertSize == 0:
        if "0x20" in flags:
            
            print("{0}\t{1}\t{2}\t-".format(z[2], z[3], int(z[3])+len(z[9])))
        else:
            print("{0}\t{1}\t{2}\t+".format(z[2], z[3], int(z[3])+len(z[9])))

f.close()

## check sequence in bed region

## https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.cgi?db=nucleotide&id=NC_002516.2&rettype=fasta&seq_start=4694811&seq_stop=4694912&strand=2&retmode=text


