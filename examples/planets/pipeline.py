import numpy as np
import seaborn as sns

from matplotlib import pyplot as plt
from functools import partial

from src.sumreader.monad import Summary
from src.sumreader.data import CSVDataset, Schema

# define dataset schema
# class attributes are `standardised` column names
# class attribute values are column names, expect to be present in dataset instance
class Planets(Schema):
    method = "method"
    number = "number"
    orbital_period = "orbital_period"
    planet_mass = "mass"
    planet_distance = "distance"
    year = "year"


# define summary functions
# with signature (Dataset, **kwargs) => matplotlib.pyplot.Figure
def non_na_histogram_planet_mass(dataset: "Dataset") -> plt.Figure:
    non_na_values = list(filter(lambda v: v == v, dataset.planet_mass))

    counts, bin_edges = np.histogram(non_na_values, bins=20)

    fig, ax = plt.subplots()
    sns.histplot(x=counts, bins=bin_edges, ax=ax)

    ax.set_title("Histogram of non-NA planet masses")

    return fig


def log_boxplot_planet_distance(dataset: "Dataset") -> plt.Figure:
    fig, ax = plt.subplots()
    sns.boxplot(x=dataset.planet_distance, ax=ax)

    ax.set_xlabel("Planet distances")
    ax.set_title("Boxplot of log of planet distances")

    ax.set_xscale("log")

    return fig


# define summary pipeline
# ONLY defines the `recipe` for data summary
# no execution will happen until a dataset instance has been passed
pipeline = Summary() >> non_na_histogram_planet_mass >> log_boxplot_planet_distance
