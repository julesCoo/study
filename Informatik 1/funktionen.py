from dataclasses import dataclass
import re

"""
Aufgabe 1

Schreiben Sie eine Funktion für die Berechnung von Dezimalgraden in Grad, Minuten und Sekunden.
Achten Sie dabei besonders darauf, dass sowohl Alt- als auch Neugradfunktionieren (siehe vorige Übung)!
"""


# Encapsulates the different parts of an angle (degrees, minutes, seconds) in a single object.
# When converted into a string, it will be formatted as dd°mm'ss.sss".
@dataclass
class FormattedAngle:
    degrees: int
    minutes: int
    seconds: float

    def __str__(self) -> str:
        return f"{self.degrees}°{self.minutes}'{self.seconds:.3f}\""


# Generalized function for formatting angular units (degrees, radians, or whatever else people come up with in the future).
# This function is not meant to be called directly, but is used internally by the `format_grd` and `format_deg` functions.
def _format_angular_units(
    unit_value: float,
    units_per_rotation: float = 360,
    units_per_minute: float = 60,
    units_per_second: float = 60,
) -> FormattedAngle:
    # Ensure that the angle is in the range [0, units_per_rotation)
    # note that the modulo operator also converts a negative value into a positive one!
    unit_value = unit_value % units_per_rotation

    # Split it into an integer and a fractional part
    deg_int = int(unit_value)
    deg_frac = unit_value - deg_int

    # Calculate minutes from the fractional part.
    # Minutes must also be an integer, the remaining fractions are converted into seconds.
    min = deg_frac * units_per_minute
    min_int = int(min)
    min_frac = min - min_int

    # Seconds will be given in decimals, as they can no longer be broken down into smaller units.
    sec = min_frac * units_per_second

    return FormattedAngle(deg_int, min_int, sec)


# Converts a decimal value of degrees into a FormattedAngle.
def format_deg(degrees: float) -> FormattedAngle:
    return _format_angular_units(degrees, 360, 60, 60)


# Converts a decimal value of gradians into a FormattedAngle.
def format_grd(gradians: float) -> FormattedAngle:
    return _format_angular_units(gradians, 400, 100, 100)


# Converts the input of an angular unit into a FormattedAngle.
# The input should be a number followed by `deg` to indicate degrees, or `grd` to indicate gradians.
def format_angular_input(input_str: str) -> FormattedAngle:
    # Extract the number and the unit from the input string using regular expressions.
    match = re.match(r"([\+\-]?\d+\.?\d*) *(\D+)", input_str)

    if match is None:
        raise ValueError(
            "Invalid input format. Please enter a number followed by 'deg' or 'grd'."
        )

    value = float(match.group(1))
    unit = match.group(2)
    if unit == "deg":
        return format_deg(value)
    elif unit == "grd":
        return format_grd(value)
    else:
        raise ValueError("Invalid unit. Please enter 'deg' or 'grd'.")


"""
Aufgabe 2

Schreiben Sie eine Python Funktion, die die Zahlen der Fibonacci Reihe berechnet.
Die Fibonacci-Reihe ist eine Folge von Zahlen, die entsteht, indem man die beidenvorhergehenden Zahlen der Folge addiert:
  0, 1, 1, 2, 3, 5, 8, 13, 21, ...

Die ersten beiden Elemente werden dabei fix als 0 und 1 festgelegt.
Die Berechnung soll nach der Ermittlung von n Elementen abgebrochen werden
"""


def fibonacci(n: int = 10) -> list[int]:
    # The first two elements are fixed
    fib_numbers = [0, 1]

    # Calculate the remaining elements
    for i in range(2, n):
        fib_numbers.append(fib_numbers[i - 1] + fib_numbers[i - 2])

    return fib_numbers


"""
Anschließend soll jede Funktion (mit beliebigen Übergabewerten) zumindest ein
Mal aufgerufen sowie die Rückgabewerte über die Konsole ausgegeben werden.
"""

# We can't ask the user for input here, as this file is meant to be imported as a module,
# and should not produce any side-effects during import.
#
# The input/output is instead delegated to modul_import.py
