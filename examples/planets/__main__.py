from src.sumreader.data import PandasDataset
from examples.planets.pipeline import pipeline, Planets

# run summary pipeline with planets dataset
# results will be found in a folder with the same name as the schema name
# in our case, `Planets`
pipeline << PandasDataset(schema=Planets).get(
    "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/planets.csv"
)
