import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

filename = sys.argv[1]
sampleID = sys.argv[2]
# read sample data
df = pd.read_csv(filename, header=0, sep="\t")

df = df.iloc[:,0:4]
# -log_10(pvalue)
#df['AF'] = -np.log10(df.mut_AF)
df['AF'] = df.mut_AF
df.chromosome = df.chromosome.astype('category')
df.Color=df.Color.astype('category')
#df.chromosome = df.chromosome.cat.set_categories(['ch%i' % i for i in range(2,7)], ordered=True)
df = df.sort_values('chromosome')

# How to plot gene vs. -log10(pvalue) and colour it by chromosome?
df['ind'] = range(len(df))

df_grouped = df.groupby(('chromosome'))

fig = plt.figure(figsize = (22, 6))
ax = fig.add_subplot(111)
#colors = ['red','green','blue', 'yellow']
x_labels = []
x_labels_pos = []
for num, (name, group) in enumerate(df_grouped):
    print(name, group)
    #group.plot(kind='scatter', x='ind', y='minuslog10pvalue',color=colors[num % len(colors)], ax=ax)
    #group.plot(kind='scatter', x='ind', y='minuslog10pvalue', c = 'Color', ax=ax)
    group.plot(kind='scatter', x='ind', y='AF', c = group['Color'], ax=ax)
    x_labels.append(name)
    x_labels_pos.append((group['ind'].iloc[-1] - (group['ind'].iloc[-1] - group['ind'].iloc[0])/2))
ax.set_xticks(x_labels_pos)
ax.set_xticklabels(x_labels)
ax.set_title("%s_Mutect2_AF_Genome" % sampleID, fontsize=32)
ax.set_xlim([0, len(df)])
#ax.set_ylim([0, 3.5])
ax.set_ylim([-0.05, 0.22])
ax.set_xlabel('Chromosome', fontsize=20)

#plt.show()

fig.savefig('test_A.png', dpi=fig.dpi)
## ref  https://stackoverflow.com/questions/37463184/how-to-create-a-manhattan-plot-with-matplotlib-in-python
