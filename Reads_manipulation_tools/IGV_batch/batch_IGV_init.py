#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys

sampleINFO   = sys.argv[1]

d = {}
sampleHandle = open( sampleINFO , 'r' )
for line in sampleHandle:
    if not line.startswith("S"):
        x = line.rstrip().split('\t')
        d[x[0]+'_'+x[1]+'_'+x[2]] = x[3]
sampleHandle.close()

batchScript =open('test_all_samples', 'w')
for i in d:
    a = i.split('_')
    genomePos = int(a[2])

    batchScript.write("""new
genome hg19
load  E:\\bam_test\\FalsePositive\\bams\\{0}
snapshotDirectory E:\\bam_test\\FalsePositive\\snapshots_test

goto {1}:{2:,}-{3:,}
squish
sort strand

snapshot sample{4}.png\n\n\n""".format(d[i], a[1] , genomePos-79, genomePos+78, i ))

batchScript.write("exit\n")
batchScript.close()    
