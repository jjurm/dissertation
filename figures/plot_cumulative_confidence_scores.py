import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import cm, colors

import matplotlib
from matplotlib.ticker import MultipleLocator, PercentFormatter
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
                for _, row in df.iterrows()]).reset_index().rename({0: "dataset", 'index': 'weight'}, axis=1)[
    ['dataset', 'weight']]
df['weight'] = df['weight'].astype(float) / 1000
df['dataset'] = pd.Categorical(df['dataset'], categories=datasets, ordered=True)

intervals, boundaries = pd.cut(df['weight'], np.linspace(0.15, 1, num=85 + 1, endpoint=True), right=False, retbins=True)
df['bin'] = intervals.apply(lambda interval: interval.left)

# %%

counts = df.pivot_table(index=["dataset", "bin"], columns=None, values="weight", aggfunc="count") \
    .reset_index().rename({"weight": "count"}, axis=1)

counts_rel = counts.groupby(['dataset', 'bin']).agg({'count': 'sum'}) \
    .groupby(level=0).apply(lambda x: x / float(x.sum())).reset_index()
counts_rel = counts_rel.sort_values(["dataset", "bin"], ascending=False)
counts_rel['cumsum'] = counts_rel.groupby('dataset')['count'].transform(pd.Series.cumsum)


# %%

cmap = cm.get_cmap('tab10')
norm = colors.Normalize(vmin=0, vmax=9)

plt.figure(figsize=(4.5, 3))

plt.axvspan(.6, 0.9, color='0.85')

for i, dataset in enumerate(datasets):
    data = counts_rel[counts_rel['dataset'] == dataset]
    plt.plot(
        data['bin'].astype(float),
        data['cumsum'],
        linewidth=1.7,
        color=cmap(norm(i)),
        label=dataset,
        # width=0.006,
        alpha=0.8,
    )

plt.xticks([0.15, 0.4, 0.6, 0.7, 0.9])
plt.gca().set_xticklabels(["0.15", "0.4", "0.6", "0.7", "0.9"])
plt.gca().xaxis.set_minor_locator(MultipleLocator(0.1))
plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1))
plt.grid(axis="x", which='major', linestyle=":", c="0.6")
plt.grid(axis="y", which='major')

plt.title('Cumulative confidence score distribution\nin 3 protein networks')
plt.xlabel("Confidence score threshold")
plt.ylabel("Number of edges")
plt.legend(loc="upper right")

plt.tight_layout()
plt.savefig("plot_cumulative_confidence_scores.pdf")
plt.show()
