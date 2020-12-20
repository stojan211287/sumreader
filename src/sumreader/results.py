import os
from typing import Dict, Optional

import pandas as pd
import termtables as tt


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
            elif isinstance(result_content, pd.DataFrame):
                tt.print(
                    result_content.values.tolist(),
                    header=result_content.columns.values.tolist(),
                    style=tt.styles.markdown,
                    padding=(0, 1),
                    alignment="lcr",
                )
            else:
                raise ValueError(f"Unsupported result of type {type(result_content)}")
