import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
from matplotlib import cm, colors

import matplotlib
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import MultipleLocator
from pandas import Series

from utils import datasets

matplotlib.rc('text', usetex=True)
matplotlib.rcParams['mathtext.fontset'] = 'custom'
matplotlib.rcParams['mathtext.rm'] = 'Bitstream Vera Sans'
matplotlib.rcParams['mathtext.it'] = 'Bitstream Vera Sans:italic'
prop = fm.FontProperties(fname='../fonts/JetBrainsMono-1.0.3/ttf/JetBrainsMono-Regular.ttf')
matplotlib.rcParams['mathtext.tt'] = prop.get_name()


df = pd.read_csv("../figures_gen/histogram_edges.csv")
df = pd.concat([Series(row['dataset'], row['weights'].split(';'))
           for _, row in df.iterrows()]).reset_index().rename({0: "dataset",'index':'weight'},axis=1)[['dataset','weight']]
df['weight'] = df['weight'].astype(float) / 1000

#%%

cmap = cm.get_cmap('tab10')
norm = colors.Normalize(vmin=0, vmax=9)

plt.subplots(sharex="all", sharey="all", figsize=(10,3))
gs1 = GridSpec(1,3)
gs1.update(wspace=0.12, hspace=0)

pos = 0
for dataset in datasets:
    ax = plt.subplot(gs1[pos])
    sns.distplot(
        df[df['dataset'] == dataset]['weight'],
        bins=85,
        color=cmap(norm(pos)),
        label=dataset,
        hist_kws=dict(width=0.006,alpha=0.6)
    )

    plt.margins(0.02)
    plt.xticks([0.15,0.4,0.7,0.9])
    plt.xlabel("Edge confidence score")
    plt.xlim(0.13,1.02)
    plt.ylim(0,12)
    # noinspection PyUnresolvedReferences
    ax.set_xticklabels(["0.15", "0.4", "0.7", "0.9"])
    # noinspection PyUnresolvedReferences
    ax.xaxis.set_minor_locator(MultipleLocator(0.1))
    plt.grid(axis="x",which='major')

    if pos == 0:
        plt.ylabel("Relative frequency")
    plt.legend()
    pos += 1

plt.suptitle('Confidence score distribution in protein networks')
plt.subplots_adjust(wspace=0, hspace=0, bottom=0.15, left=0.05, right=0.98)
plt.savefig("histogram_edges.pdf")
plt.show()

