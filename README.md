# Data summary lib as a Reader monad

## Sample API

### Step 1 - Define data schema  - `examples.planets.pipeline`
```python
from src.sumreader.data import Schema

# class attributes are `standardised` column names
# class attribute values are column names, expect to be present in dataset instance
class Planets(Schema):
    method = "method"
    number = "number"
    orbital_period = "orbital_period"
    planet_mass = "mass"
    planet_distance = "distance"
    year = "year"
```

### Step 2 - Define summary functions - `examples.planets.pipeline`

```python
# anything with signature e.g. (Dataset, **kwargs) => matplotlib.pyplot.Figure
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
```

### Step 3 - Construct pipeline recipe - `examples.planets.pipeline`
```python
from src.sumreader.monad import Summary

# ONLY defines the `recipe` for data summary
# no execution will happen until a dataset instance has been passed
pipeline = Summary() >> non_na_histogram_planet_mass >> log_boxplot_planet_distance
```

### Step 4 - Run pipeline with particular dataset instance - `examples.planets.__main__`
```python
from src.sumreader.data import CSVDataset
from examples.planets.pipeline import pipeline, Planets

# run summary pipeline with planets dataset
# results will be found in a folder with the same name as the schema name
# in our case, `Planets`
pipeline << CSVDataset(schema=Planets).get(
    "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/planets.csv"
)
```

## How to run
To run an example summary on the `Planets` dataset from [here](https://github.com/mwaskom/seaborn-data), simply do

```bash
pipenv install && pipenv run python -m examples.planets
```