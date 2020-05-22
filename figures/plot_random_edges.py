import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib.font_manager as fm
import seaborn as sns

import matplotlib
from matplotlib.gridspec import GridSpec

from utils import palette_robustness_light, palette_robustness, palette_robustness_dark

matplotlib.rc('text', usetex=True)
matplotlib.rcParams['mathtext.fontset'] = 'custom'
matplotlib.rcParams['mathtext.rm'] = 'Bitstream Vera Sans'
matplotlib.rcParams['mathtext.it'] = 'Bitstream Vera Sans:italic'
prop = fm.FontProperties(fname='../fonts/JetBrainsMono-1.0.3/ttf/JetBrainsMono-Regular.ttf')
matplotlib.rcParams['mathtext.tt'] = prop.get_name()

columns = ['experiment', 'robustness', 'dataset', 'metric', 'value']
metrics = ['Betweenness', 'Degree', 'Ego1Edges', 'Ego2Nodes', 'LocalClustering', 'PageRank', 'Redundancy']
datasets = ['pvivax', 'ecoli', 'yeast']
robustness_measures = ['RankIdentifiability', 'RankInstability', 'RankContinuity']
random_edges_experiment = 'random-edges'
experiments = ['paper', 'reproduce', random_edges_experiment]

# %%
# DF paper

df_paper = pd.read_excel("robustness_paper.xlsx", sheet_name=None)
sheets = ['P-RankContinuity', 'P-RankIdentifiability', 'P-RankInstability']
df_paper = pd.concat({sheet: df_paper[sheet].set_index("Metric") for sheet in sheets}, axis=1)
df_paper = df_paper.unstack().reset_index()
df_paper = df_paper.rename({"level_0": "robustness", "level_1": "dataset", "Metric": "metric", 0: "value"}, axis=1)
df_paper['robustness'] = df_paper['robustness'].str[2:]
df_paper['metric'] = df_paper['metric'].replace(
    {'Harmonic centrality': 'Harmonic', 'Ego1: edges': 'Ego1Edges', 'Local clustering': 'LocalClustering',
     'Ego1/Ego2: nodes': 'EgoRatio', 'Ego2: nodes': 'Ego2Nodes'})
df_paper['dataset'] = df_paper['dataset'].str.lower().str.strip().replace({'pvx': 'pvivax'})

df_paper = df_paper[df_paper['metric'].isin(metrics) & df_paper['dataset'].isin(datasets)]
df_paper['metric'] = pd.Categorical(df_paper['metric'], categories=metrics, ordered=True)
df_paper = df_paper.assign(experiment='paper')
df_paper = df_paper[columns]

# DF graffs

df_graffs = pd.read_excel("robustness_graffs.xlsx", sheet_name=0)
df_graffs.columns = map(str.lower, df_graffs.columns)
df_graffs = df_graffs.rename({'robustnessmeasure': 'robustness'}, axis=1)
df_graffs = df_graffs[df_graffs['experiment'].isin(experiments)]
df_graffs = df_graffs[df_graffs['metric'].isin(metrics) & df_graffs['dataset'].isin(datasets)]
df_graffs['metric'] = pd.Categorical(df_graffs['metric'], categories=metrics, ordered=True)
df_graffs = df_graffs[columns]

# DF combined

df_combined = pd.concat([df_graffs, df_paper], axis=0)
df_combined = df_combined[df_combined['robustness'].isin(robustness_measures)]

# %% Sort columns

# Decide metric order
avgs = df_combined[df_combined['experiment'] == 'reproduce'].groupby(['metric', 'robustness'], as_index=False).mean()
by_metrics = avgs.pivot_table(values='value', index='metric', columns='robustness', aggfunc='mean')
by_metrics['robustness_overall'] = by_metrics['RankIdentifiability'] - by_metrics['RankInstability']
by_metrics = by_metrics.drop(robustness_measures, axis=1)
by_metrics = by_metrics.sort_values('robustness_overall', ascending=False)
metrics_sorted = list(by_metrics.index.values)

df = df_combined.copy()
df['experiment'] = pd.Categorical(df_combined['experiment'], categories=experiments, ordered=True)
df['robustness'] = pd.Categorical(df_combined['robustness'], categories=robustness_measures, ordered=True)
df['dataset'] = pd.Categorical(df_combined['dataset'], categories=datasets, ordered=True)
df['metric'] = pd.Categorical(df_combined['metric'], categories=metrics_sorted, ordered=True)
df = df.sort_values(['experiment', 'robustness', 'dataset', 'metric'])

# %% Reproduction plot

# noinspection PyTypeChecker
fig = plt.subplots(figsize=(9, 6.2), sharex=True, squeeze=True)

gs1 = GridSpec(3, 1)
gs1.update(hspace=0.02)


# noinspection PyUnresolvedReferences
def plot_for_robustness(robustness_measure, pos):
    ax1 = plt.subplot(gs1[pos])
    data = df[df['robustness'] == robustness_measure]
    palette_experiment = {
        "paper": palette_robustness_light[robustness_measure],
        "reproduce": palette_robustness[robustness_measure],
        random_edges_experiment: palette_robustness_dark[robustness_measure],
    }
    dashes_experiment = {
        "paper": (5, 4),
        "reproduce": (1, 0),
        random_edges_experiment: (1.5, 1.5),
    }

    # for dataset in datasets:
    #     data_local = data[data['dataset'] == dataset]
    #     sns.lineplot(
    #         x=data_local['metric'],
    #         y=data_local['value'],
    #         hue=data_local['experiment'],  # .rename("\\textbf{Robustness measure}"),
    #         style=data_local['experiment'],  # .rename("\\textbf{Data source}"),
    #         estimator='mean',
    #         size=True,
    #         sizes=[0.5],
    #         legend=False,
    #         palette=palette_experiment,
    #         dashes=dashes_experiment,
    #     )
    experiment_col = data['experiment'].rename("\\textbf{experiment:}")
    sns.lineplot(
        x=data['metric'],
        y=data['value'],
        hue=experiment_col,
        style=experiment_col,
        estimator='mean',
        ci=100,
        palette=palette_experiment,
        dashes=dashes_experiment,
    )

    plt.margins(x=0.07)
    plt.gca().yaxis.set_minor_locator(plticker.MultipleLocator(0.05))
    plt.grid(color='0.8', linestyle=':', which='both', axis='both')

    plt.ylabel("Rank " + robustness_measure[4:])
    return ax1


plot_for_robustness('RankContinuity', 0)
plt.title("Validating \\texttt{random-edges} experiment agains \\texttt{reproduce} and results of The Paper,\n"
          "using 3 robustness measures on 7 metrics across 3 datasets (\\texttt{pvivax}, \\texttt{ecoli}, \\texttt{yeast})")
plt.ylim(0.115, 1.04)
plt.gca().set_xticklabels([])
plt.gca().set_xlabel(None)

plot_for_robustness('RankIdentifiability', 1)
plt.ylim(0.115, 1.04)

plot_for_robustness('RankInstability', 2)
plt.xlabel("\\textsl{Metric}")
plt.gca().yaxis.set_major_locator(plticker.FixedLocator(np.linspace(0, 1, 11)))
plt.ylim(0, 0.115)

plt.subplots_adjust(left=0.07, right=0.97, top=0.92, bottom=0.08)
plt.savefig("plot_random_edges.pdf")
plt.show()
