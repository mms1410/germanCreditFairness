import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd


FIGSIZE = (12,6)
DPI = 300

sns.set_theme(style = "whitegrid")
#----------------------------------------------------------------------------------------------------------------
def plot_categories(dataframe):
    
    categories = dataframe.select_dtypes(include="category")
    cat_melt = categories.melt(var_name = "category", value_name = "value")

    grid = sns.FacetGrid(cat_melt, col = "category", col_wrap = 4, sharex = False, sharey = False)
    grid.map(sns.countplot, "value", order = None)
    for ax in grid.axes.flatten():
        ax.tick_params(axis = "x", labelrotation=45, labelsize = 8)
        ax.tick_params(axis = "y", labelsize = 8)

    grid.set_titles(col_template="{col_name}")
    grid.set_axis_labels("", "Count")
    grid.despine(left=True)
    grid.fig.subplots_adjust(hspace = .6)
    return grid

def plot_numerical(dataframe):

    numerics = dataframe.select_dtypes(include="number")
    numerics_melt = numerics.melt(var_name = "variable", value_name = "value")
    
    grid = sns.FacetGrid(numerics_melt, col = "variable", col_wrap = 4, sharex = False, sharey = False)
    grid.map(sns.violinplot, "value", order = None)
    for ax in grid.axes.flatten():
        ax.tick_params(axis = "x", labelsize = 8)
        ax.tick_params(axis = "x", labelsize = 8)

    grid.set_titles(col_template="{col_name}")
    grid.set_axis_labels("", "Density")
    grid.despine(left=True)
    grid.fig.subplots_adjust(hspace = .6)
    return grid

value_vars = ["DI", "SPD", "EOD", "AOD", "Theil"]
def plot_boxplot_metrics(save_path: str,metrics: pd.DataFrame, id_name: str, value_vars  = ["DI", "SPD", "EOD", "AOD", "Theil"],split = False, **kwargs) -> None:
    
    metrics_melted = metrics.melt(id_vars = id_name if split else None,
                                  value_vars = value_vars,
                                  var_name = "Metric",
                                  value_name = "Value")

    if split:
        metrics_total = metrics_melted.copy()
        metrics_total[id_name] = "Total"
        metrics_combined = pd.concat([metrics_melted, metrics_total], axis = 0)
        x_col = id_name
    else:
        metrics_combined = metrics_melted
        x_col = None


    figsize = kwargs.pop("figsize",  FIGSIZE)
    plt.figure(figsize = figsize)

    sns.boxplot(x = x_col, y = "Value", hue = "Metric", data = metrics_combined, **kwargs)
    title = kwargs.pop("title", f"Fairness metrics for protected attribute '{id_name}'")
    if not split:
        plt.ylabel("Metric")
    plt.title(title)

    plt.savefig(save_path, dpi = DPI, bbox_inches = "tight")

if __name__ == "__main__":
    from pathlib import Path
    ROOT = Path.cwd()
    PATH_ASSETS =  ROOT / Path("assets")

    age_metrics = pd.read_csv(PATH_ASSETS / Path("age_metrics.csv"))
    job_metrics = pd.read_csv(PATH_ASSETS / Path("job_metrics.csv"))
    personalStatus_metrics = pd.read_csv(PATH_ASSETS / Path("personalStatus_metrics.csv"))

    if "Unnamed: 0" in job_metrics: # dirty hack
        job_metrics = job_metrics.drop(columns = "Unnamed: 0")

    # decision could be to drop hence all metrics are na and not relevant
    age_metrics = age_metrics[age_metrics["accuracy"].notna()]
    job_metrics = job_metrics[job_metrics["accuracy"].notna()]
    personalStatus_metrics = personalStatus_metrics[personalStatus_metrics["accuracy"].notna()]

    plot_boxplot_metrics(PATH_ASSETS / Path("metrics_boxplot_age.png"), age_metrics, "age")
    plot_boxplot_metrics(PATH_ASSETS / Path("metrics_boxplot_job.png"), job_metrics, "job")
    plot_boxplot_metrics(PATH_ASSETS / Path("metrics_boxplot_personalStatus"), personalStatus_metrics, "personalStatus")
                         