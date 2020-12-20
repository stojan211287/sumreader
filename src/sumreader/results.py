import os
import pandas as pd


class Dataset:
    def __init__(self):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError


class CSVDataset(Dataset):
    def __init__(self, path: str):
        self._path = path
        self._data = pd.read_csv(self._path)

    def __repr__(self):
        return str(self._data)


class Summary:
    def __init__(self, config: dict):

        self._validate(config)
        self.config = config

        self._results = set()

        self._summarise()

    def _validate(self, config: dict):
        try:
            for key in {"data"}:
                config[key]
        except KeyError:
            raise ValueError(f"A config must have the {key} key!")

    def _summarise(self):
        self._mean(column="height")

    def _mean(self, column: str) -> str:
        self._results.add(
            str(
                f"Mean of column {column} is {self.config['data'][[column]].mean()[column]}"
            )
        )

    def __repr__(self):
        return os.linesep.join(self._results)
