import argparse
from functools import partial

import numpy as np
import pandas as pd
import termplotlib as tpl
import termtables as tt

from .monad import Summary
from .results import Report


def main(args: argparse.Namespace) -> None:
    def histogram_of_height(bins: int, report: "Report") -> "Summary":
        data = report.dataset
        counts, bin_edges = np.histogram(data["height"], bins=bins)

        fig = tpl.figure()
        fig.hist(counts, bin_edges, orientation="horizontal", force_ascii=False)

        report.results.update({f"Histogram of `height` - {bins} bins": fig})
        new_report_args = {"dataset": data, "results": report.results}

        return Summary(run=lambda dataset: Report(**new_report_args))

    def show_data(report: "Report") -> "Summary":
        report.results.update({f"Dataset in question: ": report.dataset})
        new_report_args = {"dataset": report.dataset, "results": report.results}

        return Summary(run=lambda dataset: Report(**new_report_args))

    height_hist_3_bins = partial(histogram_of_height, 3)

    summary_pipeline = Summary() >> show_data >> height_hist_3_bins

    start_dataset = pd.read_csv(args.path, index_col=0).reset_index()
    summary_pipeline(dataset=start_dataset).render()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", default="./tests/data.csv", type=str)

    args = parser.parse_args()

    main(args=args)
