import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib.font_manager as fm
import seaborn as sns

import matplotlib

matplotlib.rc('text', usetex=True)
matplotlib.rcParams['mathtext.fontset'] = 'custom'
matplotlib.rcParams['mathtext.rm'] = 'Bitstream Vera Sans'
matplotlib.rcParams['mathtext.it'] = 'Bitstream Vera Sans:italic'
prop = fm.FontProperties(fname='../fonts/JetBrainsMono-1.0.3/ttf/JetBrainsMono-Regular.ttf')
matplotlib.rcParams['mathtext.tt'] = prop.get_name()


columns = ['robustness', 'dataset', 'metric', 'value']
metrics = ['Betweenness', 'Degree', 'Ego1Edges', 'Ego2Nodes', 'LocalClustering', 'PageRank', 'Redundancy']
datasets = ['pvivax', 'ecoli', 'yeast']
robustness_measures = ['RankContinuity', 'RankIdentifiability', 'RankInstability']
sources = ['graffs', 'paper']

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
df_paper = df_paper[columns]

# DF graffs

df_graffs = pd.read_excel("robustness_graffs.xlsx", sheet_name=0)
df_graffs.columns = map(str.lower, df_graffs.columns)
df_graffs = df_graffs.rename({'robustnessmeasure': 'robustness'}, axis=1)
df_graffs = df_graffs[df_graffs['experiment'] == 'reproduce'].drop('experiment', axis=1)
df_graffs = df_graffs[df_graffs['metric'].isin(metrics) & df_graffs['dataset'].isin(datasets)]
df_graffs['metric'] = pd.Categorical(df_graffs['metric'], categories=metrics, ordered=True)
df_graffs = df_graffs[columns]

# DF combined

sources_dict = {"graffs": df_graffs, "paper": df_paper}
df_combined = pd.concat(sources_dict, axis=0, names=["source"]).reset_index(level=0)

# %% Sort columns

# Decide metric order
avgs = df_combined[df_combined['source'] == 'graffs'].groupby(['metric', 'robustness'], as_index=False).mean()
by_metrics = avgs.pivot_table(values='value', index='metric', columns='robustness', aggfunc='mean')
by_metrics['robustness_overall'] = by_metrics['RankContinuity'] + by_metrics['RankIdentifiability'] - by_metrics[
    'RankInstability']
by_metrics = by_metrics.drop(robustness_measures, axis=1)
by_metrics = by_metrics.sort_values('robustness_overall', ascending=False)
metrics_sorted = list(by_metrics.index.values)

df = df_combined.copy()
df['metric'] = pd.Categorical(df_combined['metric'], categories=metrics_sorted, ordered=True)
df['robustness'] = pd.Categorical(df_combined['robustness'], categories=robustness_measures, ordered=True)
df = df.sort_values(['robustness', 'metric'])

# %% Bar plot for one robustness measure

# data = df
# r = 'RankContinuity'
# data = data[data['robustness'] == r]
# # data = data.groupby(['metric','source'], as_index=False).mean()
# graffs_only = data['source'] == 'graffs'
# paper_only = data['source'] == 'paper'
#
# plt.subplots(figsize=(8, 7))
#
# plt.subplot(211)
# sns.barplot(
#     x=data[paper_only]['metric'],
#     y=data[paper_only]['value'],
#     hue=data[paper_only]['dataset'],
#     # style=data['source'],
# )
# plt.ylim(0, 1)
# plt.title(r + " paper")
#
# plt.subplot(212)
# sns.barplot(
#     x=data[graffs_only]['metric'],
#     y=data[graffs_only]['value'],
#     hue=data[graffs_only]['dataset'],
#     # style=data['source'],
# )
# plt.ylim(0, 1)
# plt.title(r + " graffs")
#
# plt.show()

# %% Reproduction plot

plt.subplots(figsize=(8, 5))

data = df.copy()
data['source_robustness'] = data['source'].astype('string') + ", " + data['robustness'].astype('string')
data = data.sort_values(['source', 'robustness'])

palette_robustness = dict(zip(robustness_measures,
                              sns.color_palette(palette="bright", n_colors=len(robustness_measures))))
palette_robustness_light = dict(zip(robustness_measures,
                                    sns.color_palette(palette="pastel", n_colors=len(robustness_measures))))
palette_source_robustness = {
    (s + ", " + r): palette_robustness[r] if s == 'graffs' else palette_robustness_light[r]
    for r in robustness_measures for s in sources
}
dashes_source_robustness = {
    (s + ", " + r): (1, 0) if s == 'graffs' else (5, 4)
    for r in robustness_measures for s in sources
}

for dataset in datasets:
    data_local = data[data['dataset'] == dataset]
    sns.lineplot(
        x=data_local['metric'],
        y=data_local['value'],
        hue=data_local['source_robustness'],  # .rename("\\textbf{Robustness measure}"),
        style=data_local['source_robustness'],  # .rename("\\textbf{Data source}"),
        estimator='mean',
        size=True,
        sizes=[0.5],
        legend=False,
        palette=palette_source_robustness,
        dashes=dashes_source_robustness,
    )

source_robustness_col = data['source_robustness'].rename("\\textbf{source, robustness measure:}")
sns.lineplot(
    x=data['metric'],
    y=data['value'],
    hue=source_robustness_col,
    style=source_robustness_col,
    estimator='mean',
    ci=100,
    palette=palette_source_robustness,
    dashes=dashes_source_robustness,
)

plt.ylim(-0.05,1.05)
plt.margins(x=0.07)
plt.gca().yaxis.set_major_locator(plticker.FixedLocator(np.linspace(0,1,5)))
plt.grid(color='0.8', linestyle=':', which='major', axis='both')
plt.title("Comparison of results from The Paper and \\texttt{graffs} (experiment: \\texttt{reproduce}),\n"
          "including 7 metrics across 3 datasets (\\texttt{pvivax}, \\texttt{ecoli}, \\texttt{yeast})")
plt.xlabel("Metric")
plt.ylabel("Robustness value")

plt.tight_layout()
plt.savefig("plot_reproduction.pdf")
plt.show()


