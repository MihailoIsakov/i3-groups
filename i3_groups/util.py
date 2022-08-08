import subprocess


def _bash(command: list[str]) -> None:
    """
    Runs a shell command in a separate process.
    """
    command = [c.encode('utf-8') for c in command]

    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output, error = process.communicate()

    if error is not None:
        raise RuntimeError(error)


