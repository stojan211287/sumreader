import os
from typing import Dict, Optional

import pandas as pd
from matplotlib import pyplot as plt 

from enum import Enum

import io
import requests
import warnings


class Schema(Enum):
    pass

class Dataset:

    def __init__(self):
        raise NotImplementedError


class PandasDataset(Dataset):   

    def __init__(self, schema: 'Schema'):

        self._columns = (column for column in schema)

        for column in self._columns:
            setattr(self, column.name, column.value)    

    # when loading dataset, replace name attributes with values from real data
    def get(self, url: str) -> 'PandasDataset':
        # read csv from url
        data = pd.read_csv(io.StringIO(requests.get(url).content.decode('utf-8')))

        # replace Dataset attributes with column values
        for attr_name, attr_value in self.__dict__.items():
            if attr_value in data.columns:
                setattr(self, attr_name, data[attr_value].values)
            else:
                warnings.warn(f"{attr_value} (value of {attr_name} not found in columns of dataset at {url} - skipping")

        return self

    
class Report:
    def __init__(self, dataset: Dataset, results: Optional[Dict] = None):

        self.dataset = dataset

        if results is None:
            self.results = dict()
        else:
            self.results = results

    def render(self):

        # ensure results dis
        res_path = os.path.join(os.getcwd(), "results")
        os.makedirs(res_path, exist_ok=True)

        for result_name, result_content in self.results.items():
            if isinstance(result_content, plt.Figure):
                result_content.savefig(os.path.join(res_path, f"./{result_name}.png"))
            else:
                raise ValueError(f"Unsupported result of type {type(result_content)}")
