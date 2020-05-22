import pandas as pd
import matplotlib.font_manager as fm

import matplotlib

from utils import small, bf, tiny, tt, ffloat, modify_tabular, fffloat

matplotlib.rc('text', usetex=True)
matplotlib.rcParams['mathtext.fontset'] = 'custom'
matplotlib.rcParams['mathtext.rm'] = 'Bitstream Vera Sans'
matplotlib.rcParams['mathtext.it'] = 'Bitstream Vera Sans:italic'
prop = fm.FontProperties(fname='../fonts/JetBrainsMono-1.0.3/ttf/JetBrainsMono-Regular.ttf')
matplotlib.rcParams['mathtext.tt'] = prop.get_name()

metrics = ['Betweenness', 'Degree', 'Ego1Edges', 'Ego2Nodes', 'LocalClustering', 'PageRank', 'Redundancy']
# each dataset should have data only from one experiment
experiment_datasets = {
    "random-edges": ['pvivax', 'ecoli', 'yeast'],
    "unscored": ['airports', 'collab', 'citation', 'facebook', 'internet'],
}
datasets = list(d for k, l in experiment_datasets.items() for d in l)
assert (len(datasets) == len(set(datasets)))  # assert no duplicates (ambiguity)
robustness_measures = ['RankContinuity', 'RankIdentifiability', 'RankInstability']

# %%
df = pd.read_excel("robustness_graffs.xlsx")
df.columns = map(str.lower, df.columns)
df = df.rename({"robustnessmeasure": "robustness"}, axis=1)
df['metric'] = pd.Categorical(df['metric'], categories=metrics, ordered=True)
df['dataset'] = pd.Categorical(df['dataset'], categories=datasets, ordered=True)

# filter each dataset only from the appropriate experiment
df = pd.concat(list(
    df[(df['experiment'] == experiment) & (df['dataset'].isin(datasets))]
    for experiment, datasets in experiment_datasets.items()
))

# %%

def table_for_robustness(robustness_measure):
    global datasets
    data = df[df['robustness'] == robustness_measure]
    # each count should be 1
    # data.groupby(["metric", "dataset"])['value'].count()

    pivot = data.pivot_table(values="value", index="metric", columns="dataset", aggfunc="first") \
        .rename_axis(None)
    pivot.columns = pivot.columns.astype(list)
    pivot = pivot.reset_index()  # .rename({"index": }, axis=1)

    column_format = "|p{40mm}|" + "|".join(
        "c" * (len(datasets)) for experiment, datasets in experiment_datasets.items()) + "|"

    float_formatter = ffloat if robustness_measure != "RankInstability" else fffloat

    latex = pivot.to_latex(
        escape=False,
        index=False,
        # index_names=False,
        caption=robustness_measure + " of " + str(len(metrics)) + " metrics on " +
                str(len(datasets)) + " datasets (" + experiments_str + ")",
        label="tab:robustness-" + robustness_measure[4:].lower(),
        column_format=column_format,
        header=[small(bf(robustness_measure))] + [tiny(tt(col)) for col in datasets],
        formatters=[lambda v: small(v)] + [lambda v: small(ffloat(v))] * len(datasets),
    )
    latex = modify_tabular(latex, in_table=False, prefix="\scalebox{1}{\n", postfix="\n}")
    return latex


with open("robustness_graffs_tables.tex", "w") as f:
    f.write("\\begin{table}[H]\n\\setlength{\\tabcolsep}{5pt}\\renewcommand{\\arraystretch}{1}\n")

    experiments = df['experiment'].unique()
    if len(experiments) == 1:
        experiments_str = "experiment \\texttt{" + experiments[0] + "}"
    else:
        experiments_str = "experiments \\texttt{" + ("}, \\texttt{".join(experiments[:-1])) + "} and \\texttt{" + \
                          experiments[-1] + "}"
    caption = "Robustness measures \\texttt{" + ("}, \\texttt{".join(robustness_measures[:-1])) + "} and \\texttt{" + \
              robustness_measures[-1] + "} of " + str(len(metrics)) + " metrics on " \
              + str(len(datasets)) + " datasets (from " + experiments_str + ")"

    #f.write("\\caption{" + caption + "}\\label{tab:robustness_results}\n")
    for i, robustness in enumerate(robustness_measures):
        if i>0:
            f.write("\\vspace*{2mm}\n")
        # f.write("\\subfloat{")
        latex = table_for_robustness(robustness)
        f.write(latex)
        # f.write("}\n")
    f.write("\\end{table}\n")
