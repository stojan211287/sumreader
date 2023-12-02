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
        self.sample = pd.read_csv(io.StringIO(requests.get(url).content.decode("utf-8")))

        # set class params using schema from Pandas
        for column_name, column_type in self.sample.dtypes.items():
            setattr(self, column_name, column_type)

