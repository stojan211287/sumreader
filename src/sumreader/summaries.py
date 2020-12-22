import numpy as np

import termplotlib as tpl

from .monad import Summary
from .results import Report


def histogram_of_height(bins: int, report: "Report") -> "Summary":
    counts, bin_edges = np.histogram(report.dataset.person_height, bins=bins)

    fig = tpl.figure()
    fig.hist(counts, bin_edges, orientation="horizontal", force_ascii=False)

    report.results.update({f"Histogram of `height` - {bins} bins": fig})
    new_report_args = {"dataset": report.dataset, "results": report.results}

    return Summary(run=lambda dataset: Report(**new_report_args))

def show_data(report: "Report") -> "Summary":
    report.results.update({f"Dataset in question: ": report.dataset})
    new_report_args = {"dataset": report.dataset, "results": report.results}

    return Summary(run=lambda dataset: Report(**new_report_args))
