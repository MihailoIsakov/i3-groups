#! /usr/bin/env python3

import i3
from i3_groups import util


if __name__ == "__main__":
    chosen_group = util.get_option("Work on group", util.get_groups())

    outputs = set([o['name'] for o in i3.get_outputs() if o['active']])

    for ws in i3.get_workspaces():
        if ws['output'] in outputs: 
            if util.get_workspace_group(ws['name']) == chosen_group:
                util.focus_on_workspace(ws['name'])
                outputs.remove(ws['output'])
