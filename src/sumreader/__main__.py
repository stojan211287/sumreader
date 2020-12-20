from functools import partial

from .monad import Summary
from .results import Report

import pandas as pd
import argparse


def main(args: argparse.Namespace) -> None:
    def add_to_height(how_much: int, report: "Report"):
        data = report.dataset
        new_data = data.assign(height=data.height + how_much)
        return Summary(run=lambda dataset: Report(dataset=new_data))

    add_20_to_height = partial(add_to_height, 20)

    pipeline = Summary() >> add_20_to_height

    start_dataset = pd.read_csv(args.path)
    print(pipeline(dataset=start_dataset))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", default="./tests/data.csv", type=str)

    args = parser.parse_args()

    main(args=args)
