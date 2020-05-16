import seaborn as sns


columns = ['robustness', 'dataset', 'metric', 'value']
metrics = ['Betweenness', 'Degree', 'Ego1Edges', 'Ego2Nodes', 'LocalClustering', 'PageRank', 'Redundancy']
datasets = ['pvivax', 'ecoli', 'yeast']
robustness_measures = ['RankContinuity', 'RankIdentifiability', 'RankInstability']
sources = ['graffs', 'paper']


palette_robustness = dict(zip(robustness_measures,
                              sns.color_palette(palette="bright", n_colors=len(robustness_measures))))
palette_robustness_light = dict(zip(robustness_measures,
                                    sns.color_palette(palette="pastel", n_colors=len(robustness_measures))))
palette_robustness_dark = dict(zip(robustness_measures,
                                    sns.color_palette(palette="dark", n_colors=len(robustness_measures))))
palette_source_robustness = {
    (s + ", " + r): palette_robustness[r] if s == 'graffs' else palette_robustness_light[r]
    for r in robustness_measures for s in sources
}
dashes_source_robustness = {
    (s + ", " + r): (1, 0) if s == 'graffs' else (5, 4)
    for r in robustness_measures for s in sources
}


ffloat = lambda v: "%.2f" % (v)
small = lambda text: "{\\small " + text + "}"
tiny = lambda text: "{\\footnotesize " + text + "}"
tt = lambda text: "\\texttt{" + text + "}"
bf = lambda text: "\\textbf{" + text + "}"


def modify_tabular(input, prefix="", postfix=""):
    return input.replace("\\begin{tabular}", prefix + "\\begin{tabular}", 1) \
        .replace("\\end{tabular}", "\\end{tabular}" + postfix, 1)
