import i3
import subprocess

from .console_inputs import *


DELIMITER = ":"


def workspace_name(group_name: str, ws_name: str) -> str:
    return (group_name + DELIMITER + ws_name).strip()


def get_group_from_name(name: str) -> str: 
    if ":" in name: 
        return name.split(DELIMITER)[0].strip()
    else:
        return "" 


def get_ws_from_name(name: str) -> str: 
    if ":" in name: 
        split = name.split(DELIMITER)
        return ("".joint(split[1:])).strip()
    else:
        return name


def _bash(command: list[str]):
    command = [c.encode('utf-8') for c in command]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output, error = process.communicate()

    return output, error

