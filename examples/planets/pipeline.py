from src.sumreader.summaries import log_boxplot, histogram_plot, scatter_two
from src.sumreader.monad import Summary
from src.sumreader.data import PandasDataset, Schema

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


# define summary pipeline
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
