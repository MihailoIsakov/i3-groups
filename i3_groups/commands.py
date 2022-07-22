import subprocess

from .util import _bash
from .workspace import Workspace, SHARED_GROUP, WSList
from .console_inputs import get_text, get_option


def rename_workspace(): 
    new_name = get_text("Rename workspace")
    WSList().focused.rename(new_name)

def move_workspace_to_group():
    wsl = WSList()
    new_group = get_option("Move to group", wsl.groups)
    wsl.focused.change_group(new_group)


def goto_next_workspace_in_group():
    wsl = WSList()
    wsl.next_ws(wsl.focused).focus_on()


def move_container_to_workspace():
    wsl = WSList()

    # put workspaces from the active group first
    wss = [str(ws) for ws in wsl if ws.group == wsl.focused.group] + \
          [str(ws) for ws in wsl if ws.group != wsl.focused.group]

    chosen_ws = get_option("Move to workspace", wss)

    return _bash(f"i3-msg move container to workspace {chosen_ws}".split())


def change_group():
    group = get_option("Change to group", WSList().groups)
    print(f"Changing to group {group}")

    for output in WSList().outputs:
        wsl = WSList().in_groups([group]).on_output(output)
        if len(wsl) == 0:
            print(f"Did not find existing workspaces in group {group} on output {output}")
            ws_name = WSList().get_valid_name(group)
            print(f"Making workspace {ws_name} on output {output}")
            Workspace.new_workspace_on_output(group, ws_name, output) 
        else:
            print(f"Focusing on {wsl[0].name}:{wsl[0].name}")
            wsl[0].focus_on() 


def new_workspace():
    # name = get_text("Workspace name")
    active_group = WSList().focused.group
    name = WSList().get_valid_name(active_group)

    Workspace.new_workspace(active_group, name)


