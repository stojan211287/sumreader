from functools import partial

from .monad import Reader
from .results import Summary


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
