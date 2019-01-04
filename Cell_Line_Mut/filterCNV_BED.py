#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re
from glob import glob
import csv

bedFile = '66gene.bed'

genes = [ 'MTHFR', 'CDA', 'CYP4B1', 'RPM1' ,'GSTP1','SLCO1B1','VAC14', 'TP53', 'XRCC1', 'CD3EAP', 'ERCC1', 'ACYP2', 'XPC' ]

patt = re.compile('.*?\((.*?)\).*')

op_B = open(bedFile, 'r')
for line in op_B:
    if not line.startswith('#'):
        res = re.match(patt, line.strip().split('\t')[-1])
        if res:
            #print(res.group(1))
            genes.append(res.group(1))
        else:
            continue
            #print(line.strip().split('\t')[-1])
            
op_B.close()


allCSV = glob("Sample*.csv")
for filename in allCSV:
    cellLine = filename.split('_')[2]
    with open(filename, mode='r') as f, open( cellLine + '_CNV.xls', mode='w', newline='') as output_file:
        writer = csv.writer(output_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Gene','Expression','Expr Level (Z-Score)','CN Type','Minor Allele','Copy Number','CN Segment Posn.','Average Ploidy','Study Id','CNV Id'])

        reader = csv.reader(f)
        try:
            next(reader)
            for row in reader:
                GeneID = row[0].split('_')[0]
                if GeneID in genes:
                    writer.writerow(row)
            
        except csv.Error as e:
            sys.exit('file {0} , line {1}: {2}'.format(filename, reader.line_num, e))
