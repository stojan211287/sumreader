from typing import Callable, Type, Any, Optional

from functools import partial


class Dataset:
    def __init__():
        raise NotImplementedError


class Summary:
    def __init__(self, config: dict):

        self._validate(config)
        self.config = config

    def _validate(self, config: dict):
        try:
            for key in {"message", "value"}:
                config[key]
        except KeyError:
            raise ValueError(f"A config must have the {key} key!")

    def __repr__(self):
        return f"Content is {self.config}"


# Scala sig is Reader[C, A] - config is of type C, and Reader returns type A
class Reader:

    # Reader is initialized with a function run: Config => Summary
    def __init__(self, run: Optional[Callable[["Config"], "Summary"]] = None):
        if run:
            self._run = run
        else:
            self._run = lambda config: Summary(config={"message": "Hello", "value": 0})

    def __call__(self, *args, **kwargs):
        return self._run(*args, **kwargs)

    # Scala sig is def map(f: A => B): Reader[C, B]
    def map(self, f: Callable[["Summary"], "Summary"]) -> "Reader":
        # self._run(config yields type Summary A), applying f then yields type Summary B
        # thus new_run_function: Config => Summary B
        new_run_function = lambda config: f(self._run(config))
        return Reader(run=new_run_function)

    # Scala sig is def map(f: A => Reader[C, B]) -> Reader[C, B]
    def flatMap(self, f: Callable[["Summary"], "Reader"]) -> "Reader":
        # self._run(config) -> Summary A
        # f(self._run(config)) -> Reader with run: config ==> Summary B
        # thus, f(self._run(config)).run(config) is config ==> Summary B
        new_run_function = lambda config: f(self._run(config))._run(config)
        return Reader(run=new_run_function)

    def __rshift__(self, f: Callable[["Summary"], "Reader"]) -> "Reader":
        return self.flatMap(f=f)


if __name__ == "__main__":

    config = {"message": "Test config", "value": 1}

    def add_value(extra: int, summary: "Summary"):
        new_config = {
            "message": summary.config["message"],
            "value": summary.config["value"] + extra,
        }
        return Reader(run=lambda config: Summary(config=new_config))

    def multiply_value(multiple: int, summary: "Summary"):
        new_config = {
            "message": summary.config["message"],
            "value": summary.config["value"] * multiple,
        }
        return Reader(run=lambda config: Summary(config=new_config))

    first_reader = Reader(run=lambda config: Summary(config=config))

    compo_reader = (
        first_reader
        >> partial(add_value, 5)
        >> partial(add_value, 3)
        >> partial(multiply_value, 4)
    )

    print(compo_reader(config=config))
