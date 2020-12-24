# Data summary lib as a Reader monad

## Sample API

For an example look into `./examples/planets/pipeline.py` (pipeline def) and `./examples/planets/summaries.py` (custom summary defs).

### Step 1 - Define data schema 

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

### Step 2 - Define summary pipeline

```python
from src.sumreader.monad import Summary
from src.sumreader.data import PandasDataset

from examples.planets.summaries import (
    boxplot_of_planet_distance,
    histogram_of_mass,
    scatter_mass_w_distance,
)

# define custom summary function by currying
from functools import partial
mass_hist_20_bins = partial(histogram_of_mass, 20)

def run(data_url: str) -> None:

    # define summary pipeline
    summary_pipeline = (
        Summary()
        >> mass_hist_20_bins
        >> boxplot_of_planet_distance
        >> scatter_mass_w_distance
    )

    # run summary pipeline with planets dataset
    summary_pipeline << PandasDataset(schema=PlanetDatasetSchema).get(data_url)
```

## How to run

The lib `sumreader` is meant to be run as a module. To run an example summary on the `Planets` dataset from [here](https://github.com/mwaskom/seaborn-data), simply do

```bash
pipenv install && pipenv run python -m examples.planets
```
