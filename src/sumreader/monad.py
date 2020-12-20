from typing import Callable, Type, Any, Optional

from .results import Summary

# Scala sig is Reader[C, A] - config is of type C, and Reader returns type A
class Reader:

    # Reader is initialized with a function run: Config => Summary
    def __init__(self, run: Optional[Callable[["Config"], "Summary"]] = None):
        if run:
            self._run = run
        else:
            self._run = lambda config: Summary(config=config)

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
