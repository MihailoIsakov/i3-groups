import subprocess


def get_text(message): 
    command = ['rofi', '-dmenu', '-l', '0', '-p', message]

    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output, error = process.communicate()

    if error is None and output.decode() != "":
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

    if error is None and output.decode() != "":
        return output.decode().strip()
    else:
        return None
