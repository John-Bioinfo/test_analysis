#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys

resP = open(sys.argv[1], 'r')

for line in resP:
    z = line.rstrip().split('\t')
    #germlineFile = '/mnt/vol1/rendong/test/project/83gene/' + z[0] + '/3.tumor.germline_VC/total.anno_select.xls'
    #PairedFile = '/mnt/vol1/rendong/project/83gene/' + z[0] + '/3.somatic_VC/total_mutect.anno_select.xls'
    SingleTFile = '/mnt/vol1/rendong/test/project/83gene/' + z[0] + '/3.somatic_VC/total_mutect.anno_select.xls'

    #g_h = open(germlineFile,  'r')
    #g_h = open( PairedFile,  'r')
    g_h = open( SingleTFile,  'r')
    for g_line in g_h:
        #if not line.startswith('N.freq'):
        if not line.startswith('level'):
            GL = g_line.rstrip().split('\t')
            #if GL[2] + '-'+GL[3] == z[1]:
            if GL[9] + '-'+GL[10] == z[1]:
                print "%s\t%s" % (z[0], g_line.rstrip())
    g_h.close()
resP.close()

