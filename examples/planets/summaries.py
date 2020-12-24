import matplotlib.pyplot as plt
import numpy as np

import seaborn as sns
from src.sumreader.monad import Summary
from src.sumreader.data import Dataset
from src.sumreader.results import Report


def histogram_of_mass(bins: int, report: "Report") -> "Summary":
    def new_run(dataset: Dataset) -> "Report":

        non_na_planet_mass = list(filter(lambda v: v == v, dataset.planet_mass))

        counts, bin_edges = np.histogram(non_na_planet_mass, bins=bins)

        fig, ax = plt.subplots()
        sns.histplot(x=counts, bins=bin_edges, ax=ax)

        ax.set_title(f"Histogram of planet mass - using {bins} bins")

        return report.add(planet_mass_hist=fig)

    return Summary(run=new_run)


def boxplot_of_planet_distance(report: "Report") -> "Summary":
    def new_run(dataset: Dataset) -> "Report":

        fig, ax = plt.subplots()
        sns.boxplot(x=dataset.planet_distance, ax=ax)

        ax.set_xlabel("Planet mass")
        ax.set_title("Boxplot of planet mass")

        ax.set_xscale("log")

        return report.add(planet_distance_boxplot=fig)

    return Summary(run=new_run)


def scatter_mass_w_distance(report: "Report") -> "Summary":
    def new_run(dataset: Dataset) -> "Report":
        fig, ax = plt.subplots()
        sns.scatterplot(
            x=np.log1p(dataset.planet_distance), y=dataset.planet_mass, ax=ax
        )

        ax.set_xlabel("Planet distance")
        ax.set_ylabel("Planet mass")
        ax.set_title("Scatterplot of (log) planet distance vs planet mass")

        return report.add(mass_distance_scatter=fig)

    return Summary(run=new_run)
