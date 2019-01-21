#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

dep1 = sys.argv[1]  ## normal
dep2 = sys.argv[2]  ## tumor

fig, ax = plt.subplots(figsize=(10, 3))

# fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(8, 4))

# '1910007_normal_hlaA_1.dep'

data1 = pd.read_csv(dep1, sep='\t', header=None)

# '1910007_tumor_hlaA_1.dep'

data2 = pd.read_csv(dep2, sep='\t', header=None)

data1.columns = ['gene', 'pos', 'normal_dep']
data2.columns = ['gene', 'pos', 'tumor_dep']
result = pd.merge(data1, data2, how='left', on = ['gene', 'pos'])


x = result['pos']
#ax.plot(x, result['normal_dep'], label = 'Normal',linestyle= '--', color='c'  )
#ax.plot(x, result['tumor_dep'],  label = 'Tumor', linestyle= ':' , color='r'   )

ax.plot(x, result['normal_dep'], '--c'  )
ax.plot(x, result['tumor_dep'],  ':r'   )

ax.set_title('HLA gene allele 1 depth')
ax.legend(loc = 'upper left')

ax.set_xlabel('gene positon')
ax.set_xlim( left = 0, right = 3520)

plt.savefig('test_1910007_allele1.png')
