#! /usr/bin/env python3

from i3_groups import util


if __name__ == "__main__":
    group = util.get_active_group()
    name = util.get_text("Rename workspace")
    util.rename_workspace(group + ":" + name)
    
