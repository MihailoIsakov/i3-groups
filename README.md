# i3-groups

When working on multiple projects, you may find that you have tens
of workspaces over multiple monitors. Switching between projects 
requires moving to all of the monitors and 

i3-groups lets you group workspaces and cycle between workspaces 
within a group. 

# Concepts:
At all times there exists an active group, and all monitors show workspaces from the same group. 
Changing the group switches the workspace on all monitors to that group.

# Installation
```
```

# Commands:



`make-workspace`: Creates a new workspace in this group and changes focus to it. 

`rename-workspace`: Changes the name of the focused workspace. Opens a rofi menu if no name is passed.    

`move-container-to-ws`: Moves container to specified workspace and group, but keeps focus on current workspace.

`move-ws-to-group`: Moves workspace (and all containers in it) 
to a chosen group, but keeps focus on the workspace.

`change-active-group`: Changes active group, forces all monitors to select a workspace from that group with a matching
monitor. Creates new workspaces on montitors that don't have a matching group.

`next-ws-in-group`: Goes to next workspace in the group. If more than `n` seconds are spent in the new
workspace, puts the new workspace at the top of the workspace order.

`goto-special-workspace()`: Focuses on one of the special workspaces that have a
group named `shared`. The active group and the workspace order are not modified.
Switching to the next workspace will ignore shared workspaces. 

`i3-groups-polybar`: Serves as a replacement for Polybar's i3 module.
Outputs text that can be fed into a polybar script module shown
below. Displays separate lists of groups, and list of workspaces in the active
group. Highlights active group and focused workspace.

# Polybar module
```python
[module/main_i3]
type = custom/script
exec = i3-groups-polybar -m {xrandr_output}
tail = true
```

TODO:
- [x] Allow canceling actions
- [x] Remove special case for shared workspaces
- [x] Print other groups in grey
- [x] Fix issue where shared appears on only one desktop
- [ ] Fix i3.subscribe encoding error
- [ ] Autoname workspaces
- [ ] Have floating workspaces?
- [ ] When an urgent workspace exists, highlight it or it's group if it's group is not currently active
