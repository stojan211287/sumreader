from src.sumreader.data import PandasDataset
from examples.planets.pipeline import pipeline, Planets

# run summary pipeline with planets dataset
pipeline << PandasDataset(schema=Planets).get(
    "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/planets.csv"
)
