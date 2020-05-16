import pandas as pd

from utils import tt


def format_duration(t):
    t = int(round(t / 60))
    minutes = t % 60
    t //= 60
    hours = t % 24
    t //= 24
    days = t

    def comp(n, name):
        if n == 0.0:
            return None
        elif n == 1.0:
            return "1 " + name
        else:
            return ("%.0f" % n) + " " + name + "s"

    return ", ".join(filter(None, [comp(days, "day"), comp(hours, "hour"), comp(minutes, "min")]))


df = pd.read_excel("perf_experiments.xlsx") \
    .rename({"experiment": "Experiment"}, axis=1)
df['Total CPU time'] = df['time_user'].apply(format_duration)
df['n_graphs_total'] = df['n_datasets'] * df['n_graphs']
df['Avg CPU time per graph'] = (df['time_user'] / df['n_graphs_total']).apply(format_duration)

cols = ['Experiment', 'Total CPU time', 'Avg CPU time per graph']
df = df[cols]

df['Experiment'] = df['Experiment'].apply(lambda e: tt(e))


#%%

with open("perf_experiments_table.tex", "w") as f:
    f.write("")
    latex = df.to_latex(
        index=False,
        escape=False,
        column_format="|l|r|r|",
        caption="CPU Computation time of the 3 experiments evaluated by \\graffs, run on the \\texttt{rio} computing cluster (see \\autoref{sec:computing_cluster}).\n"
                "\\textsl{Total CPU time} is the sum of all times of individual CPU cores spent on evaluating the experiment, "
                "and \\textsl{Avg CPU time per graph} is that divided by $(\\text{number of datasets}) \\times (\\text{number of graphs generated from each dataset})$.",
        label="tab:perf_expriments_table",
    )
    f.write(latex + "\n")
    f.write("")

