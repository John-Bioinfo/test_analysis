#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import csv, sys

filename = sys.argv[1]

mutList = []

with open(filename, 'r') as f:
    reader = csv.reader(f)
    try:
        next(reader)
        for row in reader:
            ## if not line.startswith('Gene'):
            site = (row[-1])
            nchr = "chr" + site.split(":")[0]
            pos  = "-".join(site.split(":")[1].split(".."))
            #print(nchr + ":" + pos)
            
            mutList.append(nchr + ":" + pos)
            
    except csv.Error as e:
        sys.exit('file {0} , line {1}: {2}'.format(filename, reader.line_num, e))


from pyliftover import LiftOver

lo = LiftOver('hg38ToHg19.over.chain.gz')

for i in mutList:
    x = i.split(":")
    cname = x[0]
    newcor = x[1].split("-")
    cor_start = newcor[0]
    cor_end   = newcor[1]
    
    n_s = lo.convert_coordinate(cname, int(cor_start))
    n_e = lo.convert_coordinate(cname, int(cor_end))
    
    print('{0}:{1}-{2}'.format(cname, n_s[0][1], n_e[0][1]))
