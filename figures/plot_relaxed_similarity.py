import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

import matplotlib
from matplotlib.ticker import MultipleLocator

matplotlib.rc('text', usetex=True)
matplotlib.rcParams['mathtext.fontset'] = 'custom'
matplotlib.rcParams['mathtext.rm'] = 'Bitstream Vera Sans'
matplotlib.rcParams['mathtext.it'] = 'Bitstream Vera Sans:italic'
prop = fm.FontProperties(fname='../fonts/JetBrainsMono-1.0.3/ttf/JetBrainsMono-Regular.ttf')
matplotlib.rcParams['mathtext.tt'] = prop.get_name()

datasets = ['pvivax', 'ecoli', 'yeast']

datasets_bozhilova_colors = {
    "pvivax": "#04254A",
    "ecoli": "#FFC103",
    "yeast": "#AE2A36"
    # "#AA7893"
}

# %%

df = pd.read_csv('plot_relaxed_similarity_graffs.csv')

# %%

# ?Degree LocalC ?Redundancy
# ?Ego1Edges
# Betweenness
metrics = ["Degree", "Betweenness", "LocalClustering"]

plt.subplots(figsize=(10, 3), sharey="all", nrows=1, ncols=3)


def plot_metric(metric, pos):
    ax = plt.subplot(1, len(metrics), pos)
    data = df[df['metric'] == metric]

    # noinspection PyUnresolvedReferences
    ax.axvspan(0.6, 0.9, color='0.85')
    for loc in [0, 0.25, 0.5, .75, 1]:
        plt.axhline(y=loc, color="0.75", linestyle='-', linewidth=0.5)

    sns.lineplot(
        x=data['threshold'],
        y=data['similarity'],
        hue=data['dataset'],
        palette=datasets_bozhilova_colors
    )

    plt.xlim(0.13, 1)
    plt.ylim(0, 1.02)
    plt.gca().yaxis.set_major_locator(MultipleLocator(0.25))
    plt.xticks([0.15, 0.4, 0.6, 0.7, 0.9, 1])
    plt.yticks([0, 0.25, 0.5, 0.75, 0.9, 1])

    plt.title(metric)
    plt.xlabel("Threshold")

    if pos == 1:
        plt.ylabel("$\\alpha$\\,-relaxed $k\\,$-similarity")
    else:
        plt.ylabel("")
        # noinspection PyUnresolvedReferences
        plt.setp(ax.get_yticklabels(), visible=False)
    if pos == 3:
        plt.legend(loc="upper left")

    plt.plot([0, 1], [0.9, 0.9], c="0.4", linestyle="--")

    for x in [0.15, 0.4, 0.7, 0.9]:
        plt.plot([x, x], [-1, 2], linestyle=":", c="0.6")


for i, m in enumerate(metrics):
    plot_metric(m, i + 1)

plt.tight_layout()
plt.savefig("plot_relaxed_similarity_graffs.pdf")
plt.show()
