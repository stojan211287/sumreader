# Data summary lib as a Reader monad

## Sample API

### Step 1 - Define data schema  - `examples.planets.pipeline`
```python
from src.sumreader.data import Schema

class PlanetDatasetSchema(Schema):
    method = "method"
    number = "number"
    orbital_period = "orbital_period"
    planet_mass = "mass"
    planet_distance = "distance"
    year = "year"
```

### Step 2 - Define summary pipeline - `examples.planets.pipeline`
```python
from src.sumreader.monad import Summary

from examples.planets.summaries import (
    boxplot_of_planet_distance,
    histogram_of_mass,
    scatter_mass_w_distance,
)

# define summary pipeline
pipeline = (
    Summary()
    >> histogram_of_mass
    >> boxplot_of_planet_distance
    >> scatter_mass_w_distance
)
```

### Step 3 - Run pipeline with particular dataset instance - `examples.planets.__main__`
```python
from src.sumreader.data import PandasDataset
from examples.planets.pipeline import pipeline, PlanetDatasetSchema

# run summary pipeline with planets dataset
pipeline << PandasDataset(schema=PlanetDatasetSchema).get(
    "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/planets.csv"
)
```

## How to run
To run an example summary on the `Planets` dataset from [here](https://github.com/mwaskom/seaborn-data), simply do

```bash
pipenv install && pipenv run python -m examples.planets
```
