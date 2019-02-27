#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import subprocess
import sys

targetsFile = sys.argv[1] 

fp = open(targetsFile,  'r')
for line in fp:
    if not line.startswith('S'):
        x = line.rstrip().split('\t')
        SampleDir = '/mnt/vol1/rendong/test/project/83gene/' + x[0] + '/3.somatic_VC/'

        subprocess.call('find {0} -name "*.vcf" | xargs grep "{1}*" | awk \'{{print $1}}\' | awk -F\':\' \'{{print $1}}\' >> resTargets.list'.format(SampleDir, x[2][:-1]), shell=True)
fp.close()


