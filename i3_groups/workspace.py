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

    @staticmethod
    def make_name(group: str, name: str) -> str: 
        if group is None or group == "":
            return name.strip()
        else: 
            return (group + DELIMITER + name).strip()

    @staticmethod
    def new_workspace(group, name) -> Workspace:
        full_name = Workspace.make_name(group, name) 
        return _bash(f"i3-msg workspace {full_name}".split()) 

    @staticmethod
    def new_workspace_on_output(group, name, output) -> Workspace:
        full_name = Workspace.make_name(group, name) 
        output1, error1 = _bash(f"i3-msg focus output {output}".split())
        output2, error2 = _bash(f"i3-msg workspace {full_name}".split()) 

    def __post_init__(self):
        if ":" in self.name:
            self.group = self.name.split(DELIMITER)[0].strip()
            self.name  = ("".join(self.name.split(DELIMITER)[1:])).strip()  
        else:
            self.group = "" 
            self.name  = self.name

    def __str__(self) -> str:
        return Workspace.make_name(self.group, self.name)

    def rename(self, new_name):
        old_name = str(self)
        self.name = new_name

        return _bash(f"i3-msg rename workspace {old_name} to {self}".split())

    def change_group(self, group):
        self.group = group
        return _bash(f"i3-msg rename workspace to {self}".split())

    def focus_on(self):
        return _bash(f"i3 workspace {self}".split())


   
class WSList():
    """
    Workspace list
    """
    def __init__(self):
        self._list = [Workspace(**w) for w in i3.get_workspaces()]

    def __len__(self):
        return len(self._list) 

    def __getitem__(self, idx):
        return self._list[idx]

    def __iter__(self):
        for ws in self._list:
            yield ws

    def index(self, find_ws):
        for idx, ws in enumerate(self._list):
            if ws == find_ws:
                return idx

    def __str__(self):
        return str(self._list)

    @property 
    def focused(self) -> Workspace:
        focused_wss = list(filter(lambda w: w.focused, self._list))
        if len(focused_wss) > 0:
            return focused_wss[0]
        else:
            return None

    @property
    def groups(self) -> list[str]:
        gs = list(set([w.group for w in self._list]))

        return gs

    @property
    def outputs(self) -> list[str]:
        os = list(set([w.output for w in self._list]))

        return os

    @property
    def active_groups(self) -> list[str]:
        return [ws.group for ws in self._list if ws.visible]

    def get_valid_name(self, group):
        """
        Finds smallest number that is not used in the group
        """
        names = [w.name for w in self]
        for i in range(1, 100):
            if str(i) not in names:
                return str(i)

    def in_group(self, group: str) -> WSList:
        new_wsl = copy.deepcopy(self)
        new_wsl._list = [w for w in new_wsl._list if w.group == group]
        return new_wsl 
    
    def in_groups(self, groups: list[str]) -> WSList:
        new_wsl = copy.deepcopy(self)
        new_wsl._list = [w for w in new_wsl._list if w.group in groups]
        return new_wsl 

    def on_output(self, output: str) -> WSList:
        new_wsl = copy.deepcopy(self)
        new_wsl._list = [w for w in new_wsl._list if w.output in output]
        return new_wsl 

    def next_ws(self, curr: Workspace, prev=False) -> Workspace:
        """
        Returns the next workspace on the same monitor and in the same group.
        """
        wig = self.in_groups(self.active_groups).on_output(curr.output)

        pos = wig.index(curr)
        if not prev:
            next_pos = (pos + 1) % len(wig)
        else: 
            next_pos = (pos - 1) % len(wig)

        return wig[next_pos]


