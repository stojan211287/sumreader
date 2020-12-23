from src.sumreader.monad import Summary
from src.sumreader.results import PandasDataset, Schema
from examples.planets.summaries import histogram_of_mass, boxplot_of_planet_distance

from functools import partial

# define dataset schema
class PlanetDatasetSchema(Schema):
    method = "method"
    number = "number"
    orbital_period = "orbital_period"
    planet_mass = "mass"
    planet_distance = "distance"
    year = "year"

# define custom summary function by currying
mass_hist_20_bins = partial(histogram_of_mass, 20)


def run(data_url: str) -> None:

    # define summary pipeline
    summary_pipeline = Summary() >> mass_hist_20_bins >> boxplot_of_planet_distance

    # run summary pipeline with planets dataset
    summary_pipeline << PandasDataset(schema=PlanetDatasetSchema).get(data_url)
