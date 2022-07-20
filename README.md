# i3-groups

When working on multiple projects, you may find that you have tens
of workspaces over multiple monitors. Switching between projects 
requires moving to all of the monitors and 

i3-groups lets you group workspaces and cycle between workspaces 
within a group. 

# Conecepts:
At all times there exists an active group, and all monitors show workspaces from the same group. 
Changing the group switches the workspace on all monitors to that group.

# Commands:
`rename-workspace.py`: does what it says, but maintains the group if one exists
`move-to-group.py`: moves the workspace to an existing group or creates a new one

TODO:
 - [x] script for creating new groups
    - [x] parse names to get list of groups
 - [x] script for renaming workspaces 
 - [x] script for moving workspace to group
 - [x] script for next / prev workspace on output 
 - [ ] script for changing groups
