import sys


def print_progress(name: str, done: int, total: int) -> None:
    """
    Print an updateable progress bar to the console.
    """
    bar_length = 20
    terminal_width = 80

    s = "\r["
    s += "=" * int(done / total * bar_length)
    s += " " * (bar_length - int(done / total * bar_length))
    s += "]"
    s += f" {done}/{total} - {name}"
    s += " " * (terminal_width - len(s))

    if done == total:
        s += "\n"

    sys.stdout.write(s)
    sys.stdout.flush()
