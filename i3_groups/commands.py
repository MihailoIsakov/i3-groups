import argparse
import i3

from .manager import WsManager, _bash
from .workspace import Workspace
from .console_inputs import get_text, get_option


SHARED = 'shared'


def new_workspace():
    """
    Creates a new workspace and changes focus to it.
    """
    mgr = WsManager()
    mgr.new_workspace()
    mgr.update_ordering()


def rename_workspace():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name')
    args = parser.parse_args()

    if args.name:
        name = args.name
    else:
        name = get_text("Rename workspace")

    mgr = WsManager()
    mgr.focused.change_name(name)


def move_container_to_workspace():
    mgr = WsManager()

    # put workspaces from the active group first
    # wss = [str(ws) for ws in mgr.workspaces if ws.group == mgr.active_group] + \
          # [str(ws) for ws in mgr.workspaces if ws.group != mgr.active_group]
    # wss = list(set(mgr.filter_workspaces(group=mgr.active_group) + mgr.workspaces))
    wss = mgr.sort(mgr.workspaces)

    chosen_ws = get_option("Move to workspace", [str(w) for w in wss])

    if chosen_ws is None: 
        return 

    return _bash(f"i3-msg move container to workspace {chosen_ws}".split())


def move_workspace_to_group():
    mgr = WsManager()
    new_group = get_option("Move to group", mgr.groups)

    if new_group is not None:
        mgr.focused.change_group(new_group)
        mgr.update_ordering()


def change_group():
    """
    Changes active group and switches all monitors to workspaces in that group 
    with a matching monitor.
    """
    mgr = WsManager()
    group = get_option("Change to group", mgr.groups)

    if group is None:
        return

    mgr.active_group = group

    for output in mgr.outputs:
        ws = mgr.next_workspace(group=group, output=output)
        if ws is not None:
            ws.focus()
        else:
            mgr.new_workspace(group=group, output=output)

        mgr.update_ordering()


def goto_next_workspace_in_group():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--prev', action='store_true', default=False)
    args = parser.parse_args()

    mgr = WsManager()
    offset = 1 if not args.prev else -1
    mgr.next_workspace(mgr.focused, offset=offset).focus()
    mgr.update_ordering()
        

def goto_special_workspace():
    """
    Switches to a special workspace outside of the group (e.g., a browser or note app).

    Temporarily adds the special workspace to the group so that goto_next_workspace_in_group still works.
    After the special workspace is left, it is removed from the group.
    Special workspaces are named f'{SHARED}:{key}' when they are not focused, and as
    f'{active_group}:{SHARED}_{key}' when they are focused.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--key', type=str, default=None)
    args = parser.parse_args()

    mgr = WsManager()
    mgr.new_workspace(name=args.key, group=SHARED)


def polybar():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--monitor', type=str, default=None) 
    args = parser.parse_args()

    def wrap(text, fc=None, bc=None):
        if fc is not None: 
            text = "%{F" + fc +  "}" + text + "%{F-}"
        if bc is not None: 
            text = "%{B" + bc +  "}" + text + "%{B-}"

        return text

    def print_ws(event, data, subscription):
        # active_group = WSList().focused.group
        mgr = WsManager()

        wsl = mgr.filter_workspaces(group=mgr.active_group)
        if args.monitor is not None:
            wsl = wsl.on_output(args.monitor)
        
        output = " "
        for g in mgr.groups:
            if g in mgr.active_group:
                output += wrap(g, bc="#282A2E", fc="#F0C674") + " / "
            else:
                output += wrap(g, bc="#282A2E", fc="#666666") + " / "

        output += "   " 

        for w in wsl:
            if w.visible: 
                # output += wrap(" " + w.name + " ", fc="#282A2E", bc="#F0C674")
                output += wrap(" " + w.name + " ", bc="#282A2E", fc="#F0C674")
            else:
                output += wrap(" " + w.name + " ", fc="#C5C8C6")
        
            output += "|"

        try: 
            print(output[:-3], flush=True)
        except:
            print(output, flush=True)

    try:
        subscription = i3.Subscription(print_ws, 'workspace')
    except:
        print('error')

