#!/usr/bin/env python
# -*- coding:UTF-8 -*-

__author__ = "Zongyun Qiao"
__copyright__ = "Copyright 2018, A Biotech"
__credits__ = [
    "Zongyun Qiao"]  # remember to add yourself
__license__ = "GPL"
__version__ = "0.1-dev, 20180409"
__maintainer__ = "Zongyun Qiao"
__email__ = "gulile@yeah.net"

from collections import deque

Emer =  {   "AA": -1.94,
            "AC": -1.34, 
            "AG": -1.6,
            "AT": -1.47, 
            "CA": -1.95,
            "CC": -3.07,
            "CG": -3.61,
            "CT": -1.6,
            "GA": -1.57,
            "GC": -3.14, 
            "GG": -3.07,
            "GT": -1.34,
            "TA": -0.96,
            "TC": -1.57, 
            "TG": -1.95, 
            "TT": -1.94    }
#Energy of polymer
complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}

def calcDg(list1, list2):
    m = len(list1)
    n = len(list2)
    U1 = list1.upper()
    U2 = list2.upper()
    d = deque()
    d.extendleft(U2)
    U2N = ''.join(d)
    reverse_N = "".join(complement.get(base, base) for base in U2N)
    L = set()
    for a in range(m-2):
        subU1 = U1[a:]
        subM = len(subU1)
        for a_end in range(2,subM+1):
            #L.append(subU1[:a_end])
            subNew = subU1[:a_end]
            if subNew in reverse_N:
                L.add(subNew)

    dG = []
    for b in L:
        g = 0
        for i in range(len(b)-1):
            g += Emer[b[i:i+2]]
        #dG.append("{0:.2f}".format(g))
        dG.append(g)
    return(dG)

def GCCalc(seq):
    GC_Content = seq.count("C") + seq.count("G")
    return GC_Content * 100.0 / len(seq)

def TemMelt(seq, minT, maxT):
    sGC = (seq.count("C") + seq.count("G"))*1.0 / len(seq)
    con005_T = 59.9 + 41.0 * sGC - (675.0/len(seq))

    con1_T   = 81.5 + 41.0 * sGC - (675.0/len(seq))

    if con005_T >= minT * 1.0 and con005_T <= maxT * 1.0:
        return True,  con005_T, con1_T
    else:
        return False, con005_T, con1_T

a = calcDg("ATCGgct","agccTTCAG")
for i in a:
    print("{0:.2f}".format(i))

GCtest = GCCalc("ATCGGTCG")
print(GCtest)

