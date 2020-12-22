import os
from typing import Dict, Optional

import pandas as pd
import termtables as tt

from enum import Enum


class Column(Enum):
    pass

class Dataset:

    def __init__(self):
        raise NotImplementedError


class PandasDataset(Dataset):        

    def get(self, path: str) -> 'PandasDataset':
        data = pd.read_csv(path, index_col=0).reset_index()
        for attr_name, attr_value in self.__dict__.items():
            if attr_value in data.columns:
                setattr(self, attr_name, data[attr_value].values)
        return self


class TestDataset(PandasDataset):

    def __init__(self):

        class TestDatasetColumn(Column):
            unique_id = "id"
            person_name = "name"
            person_height = "height"

        self._columns = (column for column in TestDatasetColumn)

        for column in self._columns:
            setattr(self, column.name, column.value)


class Report:
    def __init__(self, dataset: pd.DataFrame, results: Optional[Dict] = None):

        self.dataset = dataset

        if results is None:
            self.results = dict()
        else:
            self.results = results

    def render(self):
        for result_name, result_content in self.results.items():
            print(os.linesep)
            print(result_name)
            if hasattr(result_content, "show"):
                result_content.show()
            elif isinstance(result_content, Dataset):
                for name, vals in result_content.__dict__.items():
                    if not name.startswith("_"):
                        print(name)
                        print(vals)
            else:
                raise ValueError(f"Unsupported result of type {type(result_content)}")
