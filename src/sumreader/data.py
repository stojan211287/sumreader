import io

import requests
import warnings

import pandas as pd

from enum import Enum


class Schema(Enum):
    pass


class Dataset:
    def __init__(self):
        raise NotImplementedError

    def get(self, url: str) -> "Dataset":
        raise NotImplementedError


class PandasDataset(Dataset):
    def __init__(self, schema: "Schema"):

        self._columns = (column for column in schema)

        for column in self._columns:
            setattr(self, column.name, column.value)

    # when loading dataset, replace name attributes with values from real data
    def get(self, url: str) -> "PandasDataset":
        # read csv from url
        data = pd.read_csv(io.StringIO(requests.get(url).content.decode("utf-8")))

        # replace Dataset attributes with column values
        for attr_name, attr_value in self.__dict__.items():
            if attr_value in data.columns:
                setattr(self, attr_name, data[attr_value].values)
            else:
                warnings.warn(
                    f"{attr_value} (value of {attr_name} not found in columns of dataset at {url} - skipping"
                )

        return self
