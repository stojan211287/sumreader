import io

import requests
import warnings

import pandas as pd

from enum import Enum


class Config:
    def __init__(self):
        raise NotImplementedError

    def get(self, url: str) -> "Config":
        raise NotImplementedError


class PandasDataframeConfig(Config):
    # when loading Config, replace name attributes with values from real data
    def __init__(self, url: str) -> "PandasDataframeConfig":
        # read csv from url
        self.sample = pd.read_csv(
            io.StringIO(requests.get(url).content.decode("utf-8")),
            engine="pyarrow",
            dtype_backend="pyarrow"
        )

    def to_mapping(self):
        return dict(
            **{
                k: v
                for k, v in self.sample.dtypes.items()
            }
        )


import pandas 

pandas.DataFrame.to_sql