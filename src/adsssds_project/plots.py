import seaborn as sns
sns.set_theme(style = "whitegrid")

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

    