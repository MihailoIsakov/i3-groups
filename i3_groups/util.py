import i3
import subprocess


def rename_workspace(name=None):
    if name is None: 
        group = get_active_group()
        workspace = get_text("Rename workspace")
        name = group + ":" + workspace

    command = f"i3-msg rename workspace to {name}"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    return output, error


def get_text(message): 
    command = ['rofi', '-dmenu', '-l', '0', '-p', message]

    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output, error = process.communicate()

    if error is None:
        return output.decode()
    else:
        return None


def get_option(message: str, options: list[str]): 
    options = "|".join(options)
    # options = options[1:]
    c1 = ['echo', options]
    c2 = ['rofi', '-sep', '|', '-dmenu', '-p', message]

    p1 = subprocess.Popen(c1, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(c2, stdin=p1.stdout, stdout=subprocess.PIPE)
    output, error = p2.communicate()

    if error is None:
        return output.decode().strip()
    else:
        return None


def get_focused_workspace():
    workspaces = i3.get_workspaces()

    try: 
        return [w for w in workspaces if w['focused'] is True][0]
    except:
        return None


def get_focused_workspace_name():
    return get_focused_workspace()['name'].split(':')[-1]


def get_active_group():
    ws = get_focused_workspace()['name']
    if ':' in ws: 
        return ws.split(':')[0]
    else:
        return ""


def get_workspace_group(workspace):
    try: 
        if ":" in workspace: 
            group = workspace.split(":")[0]
        else: 
            group = ""
    except:
        group = ""

    return group.strip()


def get_groups():
    groups = set([""])

    for w in i3.get_workspaces():
        group = get_workspace_group(w['name'])
        groups.add(group)

    return list(groups)


def move_workspace_to_group():
    workspace = get_focused_workspace_name()

    groups = get_groups()
    groups = [""] + groups
    chosen_group = get_option("Move to group", groups).strip()

    rename_workspace(chosen_group + ":" + workspace)


def focus_on_workspace(workspace: str):
    command = f"i3 workspace {workspace}"

    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


def get_workspaces_in_group(group: str) -> list[str]:
    workspaces = i3.get_workspaces()
    group_workspaces = []

    for w in i3.get_workspaces():
        if group == w['name'][:len(group)]:
            group_workspaces.append(w['name'])

    return group_workspaces


def next_workspace_in_active_group():
    active_group = get_active_group()
    wig = get_workspaces_in_group(active_group)

    pos = wig.index(active_group + ":" + get_focused_workspace_name())
    next_pos = (pos + 1) % len(wig)

    return wig[next_pos]


def goto_next_workspace_in_group():
    ws = next_workspace_in_active_group()
    focus_on_workspace(ws)


def move_container_to_workspace():
    ws_names = [ws['name'] for ws in i3.get_workspaces()]

    # sort by group
    group = get_active_group()
    l1, l2 = [], []
    for ws in ws_names:
        if group == ws[:len(group)]:
            l1.append(ws)
        else:
            l2.append(ws)

    ws_names = l1 + l2
    
    chosen_ws = get_option("Move to workspace", ws_names)

    command = f"i3-msg move container to workspace {chosen_ws}"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


def change_group():
    chosen_group = get_option("Work on group", get_groups())

    outputs = set([o['name'] for o in i3.get_outputs() if o['active']])

    for ws in i3.get_workspaces():
        if ws['output'] in outputs: 
            if get_workspace_group(ws['name']) == chosen_group:
                focus_on_workspace(ws['name'])
                outputs.remove(ws['output'])

    

