#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import subprocess
import argparse
import os

parser = argparse.ArgumentParser(description="The USAGE")     #define usage for current script
parser.add_argument("-i", "--bamlist_file", type = str, dest='ListName', action='store', required=True)
parser.add_argument("-sn", "--sample_file", type = str)

# bamlist:  

options = parser.parse_args()

file_D = {}
h_list = open(options.ListName, 'r')
for i in h_list:
    x = i.rstrip()
    fileLabel = os.path.basename(x).split('.')[0]

    file_D[fileLabel] = x

h_list.close()

sample_Mut_File = options.sample_file
sample_num      = os.path.basename(sample_Mut_File).split('_')[0] 

if not os.path.exists('extracted_bams'):
   os.mkdir('extracted_bams')


h_sample = open(sample_Mut_File, 'r')
for i in h_sample:
    x = i.rstrip().split('\t')
    chrN  = x[0]
    position = int(x[1])
    command_1 = 'samtools view -h %s %s:%d-%d > extracted_bams/%s_%s_%d_%d.sam' % (file_D[sample_num], 
chrN, position-1500, position+1500, sample_num, chrN, position-1500, position+1500)
    subprocess.call(command_1, shell=True)    
    command_2 = 'samtools view -bS extracted_bams/%s_%s_%d_%d.sam | samtools sort -@ 8 - -T /tmp/test_sort -o extracted_bams/%s_%s_%d_%d_sorted.bam' % (sample_num, chrN, position-1500, position+1500, sample_num, chrN, position-1500, position+1500)

    subprocess.call(command_2, shell=True)    
h_sample.close()



