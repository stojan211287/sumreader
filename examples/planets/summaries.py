import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from src.sumreader.monad import Summary
from src.sumreader.results import Report


def histogram_of_mass(bins: int, report: "Report") -> "Summary":

    non_na_planet_mass = list(filter(lambda v: v==v, report.dataset.planet_mass))

    counts, bin_edges = np.histogram(non_na_planet_mass, bins=bins)

    fig, ax  = plt.subplots()
    sns.histplot(x=counts, bins=bin_edges, ax=ax)

    ax.set_title(f"Histogram of planet mass - using {bins} bins")

    report.results.update({f"Histogram of 'planet_mass' - {bins} bins": fig})
    new_report_args = {"dataset": report.dataset, "results": report.results}

    return Summary(run=lambda dataset: Report(**new_report_args))

def boxplot_of_planet_distance(report: "Report") -> "Summary":

    fig, ax  = plt.subplots()
    sns.boxplot(x=report.dataset.planet_distance, ax=ax)

    ax.set_xlabel("Planet mass")
    ax.set_title("Boxplot of planet mass")

    ax.set_xscale('log')

    report.results.update({f"Boxplot of 'planet_distnace'": fig})

    new_report_args = {"dataset": report.dataset, "results": report.results}

    return Summary(run=lambda dataset: Report(**new_report_args))

