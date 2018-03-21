#!/usr/bin/env python
# -*- coding:UTF-8 -*-

__author__ = "Zongyun Qiao"
__copyright__ = "Copyright 2018, -------- ---tech"
__credits__ = [
    "Zongyun Qiao"]  # remember to add yourself
__license__ = "GPL"
__version__ = "0.1-dev, 20180321"
__maintainer__ = "Zongyun Qiao"
__email__ = "gulile@yeah.net"

import linecache
import numpy as np
from collections import defaultdict

def data_C(numList):
    a = np.array(numList)
    return np.mean(a)

def filter_type(inputF, typeS, outPrefix = "formated_"):

    header = linecache.getline(inputF, 1)

    d = {}
    d_d = defaultdict(list)
    outH = open(outPrefix + typeS + ".xls", "w")
    
    newColNames = header.strip().split("\t")
    newHeader = "\t".join(newColNames[0:5]) + "\tDmax\tDmin\t" + "\t".join(newColNames[13:18]) + "\treadSS"
    outH.write(newHeader + "\n")
    
    handle_In = open(inputF, "r")
    for line in handle_In:
        if line.startswith("probe_name"):
            continue
            ## outH.write(line) 
        else:
            y = line.strip().split("\t")

            keyP = y[0] +"__" + y[10]
            if y[4] == typeS:
                if keyP not in d:
                    d[keyP] = "\t".join(y[1:5]) + "\t" +"\t".join(y[11:18])
                d_d[keyP].append("\t".join(y[5:10]))
                
                
    for i in d:
        probe = i.split("__")
        
        probe_values = d[i].split("\t")
        
        Dmax_v      =  probe_values[4].strip("\"")
        Dmin_v      =  probe_values[5].strip("\"")
        
        Dmax_L      =  [float(v.split(":")[1]) for v in Dmax_v.split(",")]
        Dmin_L      =  [float(v.split(":")[1]) for v in Dmin_v.split(",")]
        
        Dmax    =  data_C(Dmax_L)
        Dmin    =  data_C(Dmin_L)
        
        ##outH.write(probe[0] + "\t" + d[i] + "@@".join(d_d[i]) + "\n")
        outH.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(probe[0], "\t".join(probe_values[0:4]), Dmax, Dmin, \
            "\t".join(probe_values[6:]), "@@".join(d_d[i]) ))
    outH.close()

if __name__ == "__main__":    
    filter_type("result_final.txt", "gDNA")

