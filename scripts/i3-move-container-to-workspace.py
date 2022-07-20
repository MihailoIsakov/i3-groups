#! /usr/bin/env python3

import i3
from i3_groups import util


if __name__ == "__main__":
    ws_names = [ws['name'] for ws in i3.get_workspaces()]

    # sort by group
    group = util.get_active_group()
    l1, l2 = [], []
    for ws in ws_names:
        if group == ws[:len(group)]:
            l1.append(ws)
        else:
            l2.append(ws)

    ws_names = l1 + l2
    
    chosen_ws = util.get_option("Move to workspace", ws_names)
    util.move_container_to_workspace(chosen_ws)

