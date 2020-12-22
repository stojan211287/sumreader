import argparse
from functools import partial

from .monad import Summary
from .results import PandasDataset, Schema
from .summaries import show_data, histogram_of_height


def main(args: argparse.Namespace) -> None:

    # define test dataset schema
    class TestSchema(Schema):
        unique_id = "id"
        person_name = "name"
        person_height = "height"

    # define custom summary function by currying
    height_hist_3_bins = partial(histogram_of_height, 3)

    # define summary pipeline
    summary_pipeline = Summary() >> show_data >> height_hist_3_bins

    # run summary pipeline with test dataset
    summary_pipeline << PandasDataset(schema=TestSchema).get(args.path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", default="./tests/data.csv", type=str)

    args = parser.parse_args()

    main(args=args)
