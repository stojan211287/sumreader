from typing import Any, Callable, Optional, Type
from functools import partial
from .output import SystemCommand
from .data import Config


# Scala sig is Playbook[C, A] - Config is type C, the SystemCommand represents type A (output of processing COnfig), 
# and Playbook[C, A] is the higher-order monadic type
class Playbook:
    # Playbook is initialized with a function run: Config => SystemCommand 
    def __init__(self, run: Optional[Callable[["Config"], "SystemCommand"]] = None):
        if run:
            self._run = run
        else:
            self._run = lambda config: SystemCommand()

    # Scala sig is def map(f: A => B): Playbook[C, B]
    def map(self, f: Callable[["SystemCommand"], "SystemCommand"]) -> "Playbook":
        # self._run(Config yields type SystemCommand A)
        # applying f then yields type SystemCommand B
        # thus the sig of new_run_function is Config => SystemCommand B
        new_run_function = lambda Config: f(self._run(Config))
        return Playbook(run=new_run_function)

    # Scala sig is def map(f: A => Playbook[C, B]) -> Playbook[C, B]
    def flatMap(self, f: Callable[["SystemCommand"], "Playbook"]) -> "Playbook":
        # self._run(Config) -> SystemCommand A
        # f(self._run(Config)) -> Playbook with run: Config ==> SystemCommand B
        # thus, f(self._run(Config)).run(Config) is Config ==> SystemCommand B
        new_run_function = lambda Config: f(self._run(Config))._run(Config)
        return Playbook(run=new_run_function)
    
    def __call__(self, Config: "Config"):
        return self._run(Config).render()

    def __rshift__(self, f: Callable[["Config"], Any]) -> "Playbook":
        # add boilerplate to user-defined function
        # make its sig (SystemCommand) => Playbook
        # and the apply flatMap
        f = Playbook._boilerplate_me(f)
        return self.flatMap(f=f)

    def __lshift__(self, Config: "Config"):
        return self.__call__(Config)

    @staticmethod
    def _boilerplate_me(f: Callable) -> Callable:
        def systemcommand_to_playbook_run_function(system_command: "SystemCommand", *args, **kwargs) -> "Playbook":
            def config_to_system_command(config: Config) -> "SystemCommand":
                # wrap result of `f` (str or similar) into a SystemCommand
                return system_command.add(**{f.__name__: f(config=config, *args, **kwargs)})

            # emit a new Playbook with the run function `config_to_system_command` 
            # that returns the newly-constructed SystemCommand in the previous line
            return Playbook(run=config_to_system_command)

        # return modified function - NOW WITH BOILERPLATE
        return systemcommand_to_playbook_run_function
