import argparse

from examples.planets.pipeline import run

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--path",
        default="https://raw.githubusercontent.com/mwaskom/seaborn-data/master/planets.csv",
        type=str,
    )

    args = parser.parse_args()

    run(data_url=args.path)
