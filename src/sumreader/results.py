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
