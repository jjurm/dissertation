import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib.font_manager as fm
import matplotlib.colors as colors
import seaborn as sns

import matplotlib

matplotlib.rc('text', usetex=True)
matplotlib.rcParams['mathtext.fontset'] = 'custom'
matplotlib.rcParams['mathtext.rm'] = 'Bitstream Vera Sans'
matplotlib.rcParams['mathtext.it'] = 'Bitstream Vera Sans:italic'
prop = fm.FontProperties(fname='../fonts/JetBrainsMono-1.0.3/ttf/JetBrainsMono-Regular.ttf')
matplotlib.rcParams['mathtext.tt'] = prop.get_name()

columns = ['robustness', 'dataset', 'metric', 'value']
metrics = ['Betweenness', 'Degree', 'Ego1Edges', 'Ego2Nodes', 'EgoRatio', 'LocalClustering', 'PageRank', 'Redundancy']
datasets = ['pvivax', 'ecoli', 'yeast']
robustness_measures = ['RankContinuity', 'RankIdentifiability', 'RankInstability']
sources = ['graffs', 'paper']

# %%

df = pd.read_csv("../figures_gen/plot_edge_deletion_per_step.csv")
df['threshold'] = df['threshold'] / 1000
df['deleted'] = df['deleted'] * 100 * (-1)

# %%

plt.figure(figsize=(4.5, 3))

palette_map = dict(zip(datasets, sns.color_palette(n_colors=len(datasets))))
palette_map_light = {k: colors.to_rgba(c, 0.15) for k, c in palette_map.items()}

avgs = df.groupby("dataset", as_index=False)['deleted'].mean().set_index('dataset').to_dict()['deleted']
total_avg = np.average(list(avgs.values()))

thresholds = np.linspace(df['threshold'].min(), df['threshold'].max(), 30)
for dataset in datasets:
    data = df[df['dataset'] == dataset]
    avg = avgs[dataset]
    plt.plot(
        thresholds, data['deleted'],
        color=palette_map[dataset], linewidth=1,
        label=dataset
    )
    plt.plot(
        thresholds, np.repeat(avg, 30),
        color=palette_map[dataset], ls="--", linewidth=0.5,
    )
    plt.fill_between(
        thresholds, data['deleted'], np.repeat(avg, 30),
        color=palette_map_light[dataset],
    )
plt.plot(
    thresholds,
    np.repeat(total_avg, 30),
    color="0.0",
    ls="--",
    label='average $\\approx 4\\%$'
)

leg = plt.legend(prop={'size': 10}, ncol=2)
for legobj in leg.legendHandles:
    legobj.set_linewidth(1.0)
plt.gca().xaxis.set_minor_locator(plticker.MultipleLocator(0.01))
plt.gca().yaxis.set_major_locator(plticker.MultipleLocator(1))
plt.grid(which="both", color="0.9")
plt.ylim(-10, 0)
plt.gca().yaxis.set_major_formatter(plticker.PercentFormatter(decimals=0))
plt.title("Relative change in number of edges at each threshold\nin 3 protein networks")
plt.xlabel("Threshold")
plt.ylabel("Relative $\delta$")

plt.tight_layout(pad=0.6)
plt.savefig("plot_edge_deletion_per_step.pdf")
plt.show()
