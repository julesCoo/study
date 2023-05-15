import sys


def print_progress(name: str, done: int, total: int) -> None:
    bar_length = 20
    filled_length = int(round(bar_length * done / float(total)))
    bar = "#" * filled_length + "-" * (bar_length - filled_length)
    sys.stdout.write(f"\r{name} [{bar}] {done}/{total}")
    sys.stdout.flush()
