# Data summary lib as a Reader monad

## Sample API

### Step 1 - Define data schema  - `examples.planets.pipeline`
```python
from src.sumreader.data import Schema

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
```

### Step 2 - Define summary pipeline - `examples.planets.pipeline`
```python
from src.sumreader.monad import Summary
from src.sumreader.summaries import log_boxplot, histogram_plot, scatter_two

# ONLY defines the `recipe` for data summary
# no execution will happen until a dataset instance has been passed
pipeline = (
    Summary()
    >> histogram_plot.but(
        title="Histogram of planet masses", bins=20, column="planet_mass"
    )
    >> log_boxplot.but(title="Boxplot of planet distances", column="planet_distance")
    >> scatter_two.but(
        title="Scatterplot of planet_distances vs planet mass",
        x="planet_distance",
        y="planet_mass",
    )
)
```

### Step 3 - Run pipeline with particular dataset instance - `examples.planets.__main__`
```python
from src.sumreader.data import PandasDataset
from examples.planets.pipeline import pipeline, Planets

# run summary pipeline with planets dataset
# results will be found in a folder with the same name as the schema name
# in our case, `Planets`
pipeline << PandasDataset(schema=Planets).get(
    "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/planets.csv"
)
```

## How to run
To run an example summary on the `Planets` dataset from [here](https://github.com/mwaskom/seaborn-data), simply do

```bash
pipenv install && pipenv run python -m examples.planets
```

## Adding summaries
Summary functions for constructing the pipeline are in `./src/sumreader/summaries.py`

### Example - histogram of non-NA values

```python
@Summary._boilerplate_me
def histogram_plot(
    dataset: "Dataset", column: str, title: str, bins: int
) -> plt.Figure:
    non_na_values = list(filter(lambda v: v == v, getattr(dataset, column)))

    counts, bin_edges = np.histogram(non_na_values, bins=bins)

    fig, ax = plt.subplots()
    sns.histplot(x=counts, bins=bin_edges, ax=ax)

    ax.set_title(title)

    return fig
```

The `Summary` monadic abstraction has a `_boilerplate_me` static method. 

All the method does is convert a "summarization function" with signature
```python
(Dataset, **kwargs) => plt.Figure
``` 
into a function that is easily composable with the `Summary` monad, i.e. with signature
```python
(Report) => Summary
```
