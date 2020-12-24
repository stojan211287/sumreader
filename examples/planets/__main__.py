from src.sumreader.data import PandasDataset
from examples.planets.pipeline import pipeline, PlanetDatasetSchema

# run summary pipeline with planets dataset
pipeline << PandasDataset(schema=PlanetDatasetSchema).get(
    "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/planets.csv"
)
