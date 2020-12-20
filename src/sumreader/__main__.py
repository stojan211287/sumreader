from functools import partial

from .monad import Reader
from .results import Summary

import pandas as pd
import argparse


def main(args: argparse.Namespace) -> None:
    def add_to_height(how_much: int, summary: "Summary"):
        data = summary.config["data"]
        new_data = data.assign(height=data.height + how_much)
        return Reader(run=lambda config: Summary(config={"data": new_data}))

    pipeline = Reader() >> partial(add_to_height, 20)

    start_config = {"data": pd.read_csv(args.path)}
    print(pipeline(config=start_config))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", default="./tests/data.csv", type=str)

    args = parser.parse_args()

    main(args=args)
