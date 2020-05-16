import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib.font_manager as fm
import matplotlib.colors as colors
import seaborn as sns

import matplotlib
from matplotlib.colors import LogNorm
from pandas import Categorical

from utils import tt

matplotlib.rc('text', usetex=True)
matplotlib.rcParams['mathtext.fontset'] = 'custom'
matplotlib.rcParams['mathtext.rm'] = 'Bitstream Vera Sans'
matplotlib.rcParams['mathtext.it'] = 'Bitstream Vera Sans:italic'
prop = fm.FontProperties(fname='../fonts/JetBrainsMono-1.0.3/ttf/JetBrainsMono-Regular.ttf')
matplotlib.rcParams['mathtext.tt'] = prop.get_name()

datasets = ['pvivax', 'ecoli', 'yeast', 'airports', 'citation', 'collab', 'facebook', 'internet']

# %%

df = pd.read_excel("perf_timings.xlsx")
df.columns = map(str.lower, df.columns)

# calculate means
pivot = df.pivot_table(values="time", index="metric", columns="dataset", aggfunc="mean")

# sort datasets
# pivot = pivot.reindex(pivot.mean().sort_values(ascending=False).index, axis=1)
pivot = pivot.reindex(datasets, axis=1)

# sort metrics
metrics = pivot.mean(axis=1).sort_values(ascending=False).index
pivot.index = Categorical(list(pivot.index), categories=metrics, ordered=True)
pivot = pivot.sort_index()

# %%

data = pivot.apply(lambda s: s / 1000)
data.columns = map(tt, data.columns)
log_norm = LogNorm(vmin=data.min().min(), vmax=data.max().max())

plt.figure(figsize=(4, 3))
ax = sns.heatmap(
    data,
    cbar_kws=dict(label='log ( time in seconds )', ticks=[1e-2, 1e-1, 1, 1e1, 1e2, 1e3, 1e4]),
    norm=log_norm,
    # cbar_ticks = [math.pow(10, i) for i in range(math.floor(math.log10(data.min().min())), 1+math.ceil(math.log10(data.max().max())))]
)

plt.title("Average per-graph evaluation time of metrics", pad=12)
plt.xlabel("Dataset")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
plt.ylabel("Metric")

plt.tight_layout(pad=1.02)
plt.savefig("perf_timings_matrix.pdf")
plt.show()
