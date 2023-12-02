import numpy as np
from functools import partial

from sumreader.monad import Playbook
from sumreader.data import PandasDataframeConfig

# define SystemCommand generating functions
# with signature (Config, **kwargs) => str (representing the SQL statement to use for example)
def print_schema(config: "PandasDataframeConfig")-> str:
    output = "" 
    for col, col_type  in config.sample.dtypes.items():
        output += f"{col} {col_type},"

    return output

# define summary pipeline
# ONLY defines the `recipe` for data summary
# no execution will happen until a dataset instance has been passed
pipeline = Playbook() >> print_schema 

if __name__ == "__main__":
    pipeline << PandasDataframeConfig(url="https://raw.githubusercontent.com/mwaskom/seaborn-data/master/planets.csv")
