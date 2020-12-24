import os
from typing import Dict, Optional

from matplotlib import pyplot as plt

from .data import Dataset


class Report:
    def __init__(self, results: Optional[Dict] = None):

        # self.dataset = dataset

        if results is None:
            self.results = dict()
        else:
            self.results = results

    def add(self, **results_to_wrap):

        for result_name, result in results_to_wrap.items():
            self.results.update({result_name: result})

        return self

    def render(self):

        # ensure results dis
        res_path = os.path.join(os.getcwd(), "results")
        os.makedirs(res_path, exist_ok=True)

        for result_name, result_content in self.results.items():
            if isinstance(result_content, plt.Figure):
                result_content.savefig(os.path.join(res_path, f"./{result_name}.png"))
            else:
                raise ValueError(f"Unsupported result of type {type(result_content)}")
