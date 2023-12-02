import os
from typing import Dict, Optional

from .data import PandasDataframeConfig


class SystemCommand:
    def __init__(self, commands: Optional[Dict] = None):

        if commands is None:
            self.commands = dict()
        else:
            self.commands = commands

    def add(self, **commands_to_wrap):
        self.commands.update(commands_to_wrap)
        return self

    def render(self):
        for command_name, command_content in self.commands.items():
            print(f"{command_name} - {command_content}")
