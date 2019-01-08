#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from matplotlib.ticker import ScalarFormatter, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
import sys

plt.rcParams.update({'font.size': 15})
#ax = plt.subplot(111, xlabel='x', ylabel='y', title='title')
#for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
#             ax.get_xticklabels() + ax.get_yticklabels()):
#    item.set_fontsize(20)

depfile = sys.argv[1]
fh = open(depfile,  'r')

pos = []
depth = []
for line in fh:
    z = line.strip().split()
    pos.append(int(z[1]))
    depth.append(int(z[2]))

x = np.arange(min(pos), max(pos) + 1)
for num, i in enumerate(x):
    if i not in pos:
        depth.insert(num, 0)

y = np.array(depth)

fig, ax = plt.subplots(figsize=(16, 9))

ax.plot(x, y, label='HLA-A depth')

xmin = min(x)
step = (max(x) - xmin) // 19
new_ticks1 = np.arange(xmin, xmin + (step +1) * 20, step)

##new_ticks1 = np.linspace(min(x),max(x),20)  
plt.xticks(new_ticks1, rotation = 45)

ax.set_xlabel('Genomic location in the gene region')
ax.set_ylabel('Depth of genomic position')
fig.suptitle('Distribution of depth along the gene region', 
 fontsize='25')

ax.xaxis.set_major_formatter(FormatStrFormatter('%0.0f'))
plt.savefig(depfile.replace('.dep', '') +'_depth.png')
