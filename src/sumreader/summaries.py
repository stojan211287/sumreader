import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from src.sumreader.monad import Summary
from src.sumreader.data import Dataset
from src.sumreader.results import Report


@Summary._boilerplate_me
def histogram_plot(
    dataset: "Dataset", column: str, title: str, bins: int
) -> plt.Figure:
    non_na_values = list(filter(lambda v: v == v, getattr(dataset, column)))

    counts, bin_edges = np.histogram(non_na_values, bins=bins)

    fig, ax = plt.subplots()
    sns.histplot(x=counts, bins=bin_edges, ax=ax)

    ax.set_title(title)

    return fig


@Summary._boilerplate_me
def log_boxplot(dataset: "Dataset", column: str, title: str) -> plt.Figure:
    fig, ax = plt.subplots()
    sns.boxplot(x=getattr(dataset, column), ax=ax)

    ax.set_xlabel(column)
    ax.set_title(title)

    ax.set_xscale("log")

    return fig


@Summary._boilerplate_me
def scatter_two(dataset: "Dataset", title: str, x: str, y: str) -> plt.Figure:
    fig, ax = plt.subplots()
    sns.scatterplot(x=getattr(dataset, x), y=getattr(dataset, y), ax=ax)

    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(title)

    return fig
