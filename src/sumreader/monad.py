from typing import Any, Callable, Optional, Type
from functools import partial
from .results import Dataset, Report

from matplotlib import pyplot as plt


# Scala sig is Summary[C, A] - Dataset is type C, the Report represents type A, and Summary[C, A] is the higher-order monadic type
class Summary:
    @staticmethod
    def _boilerplate_me(f: Callable) -> Callable:
        def report_to_summary_func(report: "Report", *args, **kwargs) -> "Summary":
            def data_to_report(dataset: Dataset) -> "Report":
                # wrap result of `f` (plt.Figure) into a Report
                return report.add(**{f.__name__: f(dataset=dataset, *args, **kwargs)})

            # emit a new Summary with the run function `data_to_report` that returns the newly-contstructed report in the previous line
            return Summary(run=data_to_report)

        # add partial app convenience method to `report_to_summary_func`
        def _will_be(**kwargs):
            return partial(report_to_summary_func, **kwargs)

        setattr(report_to_summary_func, "but", _will_be)

        # return modified function - NOW WITH BOILERPLATE
        return report_to_summary_func

    # Summary is initialized with a function run: Dataset => Report
    def __init__(self, run: Optional[Callable[["Dataset"], "Report"]] = None):
        if run:
            self._run = run
        else:
            self._run = lambda dataset: Report()

    def __call__(self, dataset: "Dataset"):
        return self._run(dataset).render(into=dataset._schema.__name__)

    # Scala sig is def map(f: A => B): Summary[C, B]
    def map(self, f: Callable[["Report"], "Report"]) -> "Summary":
        # self._run(Dataset yields type Report A), applying f then yields type Report B
        # thus new_run_function: Dataset => Report B
        new_run_function = lambda dataset: f(self._run(dataset))
        return Summary(run=new_run_function)

    # Scala sig is def map(f: A => Summary[C, B]) -> Summary[C, B]
    def flatMap(self, f: Callable[["Report"], "Summary"]) -> "Summary":
        # self._run(Dataset) -> Report A
        # f(self._run(Dataset)) -> Summary with run: Dataset ==> Report B
        # thus, f(self._run(Dataset)).run(Dataset) is Dataset ==> Report B
        new_run_function = lambda dataset: f(self._run(dataset))._run(dataset)
        return Summary(run=new_run_function)

    def __rshift__(self, f: Callable[["Report"], "Summary"]) -> "Summary":
        return self.flatMap(f=f)

    def __lshift__(self, dataset: "Dataset"):
        return self.__call__(dataset)
