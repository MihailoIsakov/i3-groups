import subprocess
import time
import shelve
import i3


from .util import _bash
from .workspace import Workspace


SHARED = "shared"
WAIT = 1


class Group(str):
    pass


class Output(str):
    pass


class WsStore():
    def __init__(self, db_path, mgr: 'WsManager'):
        """
        Checks whether all dictionary elements are initialized and creates
        them if not.
        """
        self.db_path = db_path
        self.mgr     = mgr

        with shelve.open(self.db_path, writeback=True) as db:
            if 'active_group' not in db:
                db['active_group'] = SHARED
            if 'order' not in db:
                db['order'] = []

    @property
    def active_group(self) -> str:
        with shelve.open(self.db_path, writeback=True) as db:
            return db['active_group']

    @active_group.setter
    def active_group(self, new_group: Group) -> None:
        with shelve.open(self.db_path, writeback=True) as db:
            db['active_group'] = new_group

    @property
    def order(self):
        # clean up order on every run
        with shelve.open(self.db_path, writeback=True) as db:
            print(f"Order: {db['order']}")
            for w in db['order']:
                if w not in self.mgr.workspaces:
                    db['order'].remove(w)

            return db['order']

    def push_ws(self, ws: Workspace) -> None:
        print('push')
        with shelve.open(self.db_path, writeback=True) as db:
            print('check')
            if ws in db['order']:
                print('is inside')
                db['order'].remove(ws)
            db['order'].insert(0, ws)
                

class WsManager():
    """
    Stores information not kept directly in i3, e.g., the active group, 
    the last workspace, the workspace access order, etc.

    Shelf contents:
        - active group
        - workspace order
        - last workspace accessed

    Note: After updates to the tree, the WsManager data is outdated.
    """
    def __init__(self, db_path='/tmp/i3_groups.pkl'):
        self.store = WsStore(db_path, mgr=self)

    def update_ordering(self):
        """
        Waits N seconds and if the focused workspace hasn't changed, 
        updates the workspace ordering with the focused workspace on top.
        """
        old_ws = self.focused 
        time.sleep(WAIT)

        if old_ws == self.focused:
            self.store.push_ws(old_ws)

    @property
    def workspaces(self, group: Group = None, output: Output = None) -> list[Workspace]:
        return [Workspace(**w) for w in i3.get_workspaces()]

    def filter_workspaces(self, group: Group = None, output: Output = None) -> list[Workspace]:
        wss = [Workspace(**w) for w in i3.get_workspaces()]

        if group is not None:
            wss = filter(lambda ws: ws.group == group, wss)

        if group is not None:
            wss = filter(lambda ws: ws.output == output, wss)

        return list(wss)

    @property
    def groups(self) -> list[Group]:
        return list(set([w.group for w in self.workspaces]))
    
    @property
    def outputs(self) -> list[Output]:
        return list(set([w.output for w in self.workspaces]))

    @property
    def active_group(self) -> str:
        self.store.active_group

    @active_group.setter
    def active_group(self, new_group: Group) -> None:
        self.store.active_group = new_group

    @property
    def order(self) -> list[Workspace]:
        return self.store.order

    @property
    def focused(self) -> Workspace:
        focused_wss = list(filter(lambda w: w.focused, self.workspaces))
        if len(focused_wss) > 0:
            return focused_wss[0]
        else:
            return None

    def get_valid_name(self, group: Group=None) -> str:
        """
        Finds smallest number that is not used in the group.
        """
        if group is None:
            group = self.active_group

        names = [w.name for w in self.workspaces]
        for i in range(1, 100):
            if str(i) not in names:
                return str(i)

    def sort(self, wslist: list[Workspace]):
        """
        Given a list of workspaces, sorts them by the current order.
        """
        order  = self.order
        order  = [ws for ws in order if ws in wslist]
        order += [ws for ws in wslist if ws not in order]

        assert len(order) == len(wslist)

        return order

    def next_workspace(self, curr: Workspace = None, group: Group = None, output: Output = None, offset: int = 1) -> Workspace:
        """

        Returns the next workspace on the same monitor and in the same group.

        First cycles through the groups in the order, then the rest.
        """
        # passing a workspace implies the group and output
        if curr is not None:
            group = curr.group
            output = curr.output

        # matching_wss = list(filter(lambda ws: ws.group == group and ws.output == output, self.workspaces))
        matching_wss = self.filter_workspaces(group=group, output=output)
        ordered_matching_wss = self.sort(matching_wss)

        # find workspace position in the current order
        if curr is not None:
            position = ordered_matching_wss.index(curr)
            next_position = (position + offset) % len(matching_wss)
        else:
            next_position = 0

        return ordered_matching_wss[next_position]

    """

    Commands sent to i3-msg.

    """
    def focus_output(self, output: Output) -> Workspace:
        _bash(f"i3-msg focus output {output}".split())

    def new_workspace(self, *, name=None, group=None, output=None) -> None:
        if group is None:
            group = self.active_group

        if name is None:
            name = self.get_valid_name(group=group)

        if output is not None: 
            self.focus_output(output)

        full_name = Workspace.make_name(group, name)
        _bash(f"i3-msg workspace {full_name}".split())

    def move_container_to_workspace(self, ws: Workspace) -> None:
        _bash(f"i3-msg move container to workspace {ws}".split())


