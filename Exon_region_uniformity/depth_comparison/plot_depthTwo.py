#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

dep1 = sys.argv[1]  ## normal
dep2 = sys.argv[2]  ## tumor

dep_a1 = sys.argv[3]
dep_a2 = sys.argv[4]

fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(12, 8))

# '1910007_normal_hlaA_1.dep'

data1 = pd.read_csv(dep1, sep='\t', header=None)

# '1910007_tumor_hlaA_1.dep'

data2 = pd.read_csv(dep2, sep='\t', header=None)

data1.columns = ['gene', 'pos', 'normal_dep']
data2.columns = ['gene', 'pos', 'tumor_dep']
result = pd.merge(data1, data2, how='left', on = ['gene', 'pos'])

x1 = result['pos']


#frames = [df1, df2, df3]

#result = pd.concat(frames, keys=['x', 'y', 'z'])
#result = pd.concat([df1, df4], ignore_index=True)
#result = pd.concat([df1, s1], axis=1, ignore_index=True)

A_d1 = pd.read_csv(dep_a1, sep='\t', header=None)
A_d2 = pd.read_csv(dep_a2, sep='\t', header=None)

A_d1.columns = ['gene', 'pos', 'normal_Allele']
A_d2.columns = ['gene', 'pos', 'tumor_Allele']

resA = pd.merge(A_d1, A_d2, how='left', on = ['gene', 'pos'])
x2   = resA['pos']


ax1.plot(x1, result['normal_dep'], '--c'  )
ax1.plot(x1, result['tumor_dep'],  ':r'   )

ax1.set_title('HLA gene allele 1 depth')
ax1.legend(loc = 'upper left')

#ax1.set_xlabel('gene positon')
ax1.set_xlim( left = 0, right = 3520)



ax2.plot(x2, resA['normal_Allele'], '--b'  )
ax2.plot(x2, resA['tumor_Allele'],  ':g'   )

ax2.set_title('HLA gene allele 2 depth')
ax2.legend(loc = 'upper left')

ax2.set_xlabel('gene positon')
ax2.set_xlim( left = 0, right = 3520)


plt.savefig('test_1910007.png')

## https://realpython.com/python-matplotlib-guide/
