from __future__ import annotations
from dataclasses import dataclass
import copy
import i3


from .util import _bash


DELIMITER = ":"


@dataclass
class Workspace():
    id: int
    num: int
    name: str
    visible: bool
    focused: bool
    rect: dict[str, int]
    output: str
    urgent: bool

    def __post_init__(self):
        if ":" in self.name:
            self.group = self.name.split(DELIMITER)[0].strip()
            self.name  = ("".join(self.name.split(DELIMITER)[1:])).strip()  
        else:
            self.group = "" 
            self.name  = self.name

    def __eq__(self, other: Workspace) -> bool:
        return self.name == other.name and self.group == other.group

    @staticmethod
    def make_name(group: str, name: str) -> str:
        """
        Create a valid full workspace name from a group and a name.
        """
        if group is None or group == "":
            return name.strip()
        else:
            return (group + DELIMITER + name).strip()

    def __str__(self) -> str:
        return self.make_name(self.group, self.name)

    def __repr__(self) -> str:
        return f"Workspace(group={self.group}, name={self.name})"

    """
    Commands sent to i3-msg.
    """
    def change_name(self, new_name: str) -> None:
        """
        Renames workspace and updates the data structures.
        """
        self.name = new_name
        _bash(f"i3-msg rename workspace to {self}".split())

    def change_group(self, group: Group) -> None:
        self.group = group
        return _bash(f"i3-msg rename workspace to {self}".split())

    def focus(self) -> None:
        _bash(f"i3 workspace {self}".split())
