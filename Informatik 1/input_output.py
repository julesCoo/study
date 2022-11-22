import math
from dataclasses import dataclass


@dataclass
class Entry:
    id: str  # All IDs are numbers, but we're not calculating anything with them, so it's safer to store them as strings.
    angle_x: float
    y: float


# Reads a csv-formatted file of angles, converts them into radians and calculates y from them.
# Returns a dictionary with id as key the corresponding Entry as value.
def parse_file(file_name: str) -> dict[str, Entry]:
    entries = {}

    # Read the file contents and split it up into individual lines.
    file_content = open(file_name, "r").read()
    lines = file_content.splitlines()

    # The first line contains the table header and can be skipped.
    for line in lines[1:]:
        # All other lines contain id, angle_x, unit in comma-separated format
        # (but with additional spaces! -> strip() strings).
        parts = line.split(",")

        # Ensure that the input is not malformed
        if len(parts) != 3:
            raise ValueError("Invalid line format: " + line)

        # Extract the id, value and unit from the line
        id = parts[0].strip()
        angle_x = float(parts[1].strip())
        unit = parts[2].strip()

        # Convert angle_x into radians
        if unit == "rad":
            pass  # no conversion necessary
        elif unit == "deg":
            angle_x = angle_x / 360 * math.tau
        elif unit == "gon":
            angle_x = angle_x / 400 * math.tau
        else:
            raise ValueError("Invalid unit, expected 'rad', 'deg' or 'gon'.")

        # We could also defer the calculation to the point where the user actually requests it,
        # but for something as simple as this, it's not worth the effort.
        y = math.sin(6 * angle_x - 3 * math.cos(angle_x))

        entries[id] = Entry(id, angle_x, y)

    return entries


def write_file(file_name: str, entries: dict[str, Entry]):
    with open(file_name, "w") as file:
        # Write the header
        file.write("[ID], [rad-Winkel], [y=sin(6x-3cos(x))]\n")

        # Write the entries
        for entry in entries.values():
            # To make this file human-friendly, we align the values with fixed tabular spacing.

            # right aligned, 5 characters
            file.write(entry.id.rjust(5))
            file.write(", ")

            # right aligned, 10 decimals
            file.write(f"{entry.angle_x:10.10f}")
            file.write(", ")

            # right aligned, 10 decimals
            file.write(f"{entry.y:10.10f}")
            file.write("\n")


# Read the input file and convert it into entries.
entries = parse_file("winkel.txt")

# Ask the user to inspect any number of entries, and store them for later processing.
inspected_entries = {}
while True:
    print("-------------------")
    print('Geben Sie eine ID ein (oder "fertig" zum beenden):')
    id = input()

    if id == "fertig":
        break

    entry = entries.get(id)
    if entry is None:
        print("ID wurde im Datensatz nicht gefunden. Bitte versuchen Sie es erneut.")
        continue

    print("")
    print(f"Bei der ID {id} finden sich folgende Werte:")
    print("---")
    print(f"ID = {entry.id}")
    print(f"rad = {entry.angle_x:.7f}")
    print(f"f(x) = {entry.y:.7f}")

    inspected_entries[id] = entry

# Write all inspected entries (including the calculated y value) to a new file.
write_file("winkel_y.txt", inspected_entries)
