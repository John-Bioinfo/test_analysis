#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__      = "Zongyun Qiao"
__copyright__   = "Copyright 2018, A Biotech"
__credits__     = [
    "Zongyun Qiao"]  # remember to add yourself
__license__     = "GPL"
__version__     = "0.1-dev, 20180427"
__maintainer__  = "Zongyun Qiao"
__email__       = "gulile@yeah.net"


from collections import defaultdict
from collections import Counter
import itertools
import pprint
import argparse

#a = [ "a:19", "b:123", "c:123","d:123", "e:123","f:123", "g:123", "h:123", "i:123",  "c:20", "d:20", "e:20", "f:30",  "g:35",
#       "h:61","i:35", "m:20", "n:123", "o:123", "p:123", "c:22", "d:22", "e:35", "m:35", "a:35", "q:35", "r:19", "s:19",  "t:19"
#]

#d = {}

d1 = defaultdict(list)
#for i in a:
#    x = i.split(":")
    #d[x[0]] = d.get(x[0],"") + x[1] + "--"
#    d1[x[0]].append(int(x[1]))


parser = argparse.ArgumentParser( description = "USAGE" ) 
 
parser.add_argument("-i", "--in_Sam",  action='store', help = "input file of breakpoints") 
args = parser.parse_args()

opSam = open(args.in_Sam, "r")
for line in opSam:
    if line.startswith("@"):
        continue
    else:
       ssLine = line.strip().split("\t")

       readsId = ssLine[0]
       pos     = int(ssLine[3])
       d1[readsId].append(pos)
opSam.close()

all_sites =  list(itertools.chain.from_iterable(d1.values()))

#pprint.pprint(d1, width=1)

while True:
    mc = Counter(all_sites).most_common()
    ma = filter(lambda x : mc[0][0] in d1[x], d1.keys())
    m_remain = filter(lambda x : mc[0][0] not in d1[x], d1.keys()) 
    if mc == []:
        break
    #print(mc)
    print(len(list(ma)))
    d1      = dict([(k, d1[k]) for k in m_remain ])    
    all_sites =  list(itertools.chain.from_iterable(d1.values()))

# python test_A.py -i Aln_merged_090_EML4_LE.sam


