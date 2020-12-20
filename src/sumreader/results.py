import os
import pandas as pd


class Report:
    def __init__(self, dataset: pd.DataFrame):

        self.dataset = dataset

        self._results = set()

        self._summarise()

    def _summarise(self):
        self._mean(column="height")

    def _mean(self, column: str) -> str:
        self._results.add(
            str(f"Mean of column {column} is {self.dataset[[column]].mean()[column]}")
        )

    def __repr__(self):
        return os.linesep.join(self._results)
