"""
Aufgabe 1

Schreiben Sie eine Funktion für die Berechnung von Dezimalgraden in Grad, Minuten und Sekunden.
Achten Sie dabei besonders darauf, dass sowohl Alt- als auch Neugradfunktionieren (siehe vorige Übung)!
"""


# Converts the input of an angular unit into a tuple of (degrees, minutes, seconds).
# The input should be a number followed by `deg` to indicate degrees, or `grd` to indicate gradians.
def convert_angular_input(input_str: str) -> tuple[int, int, float]:

    # Generalized function for formatting angular units (degrees, radians, or whatever else people come up with in the future).
    def _format_angular_units(
        unit_value: float,
        units_per_rotation: float = 360,
        units_per_minute: float = 60,
        units_per_second: float = 60,
    ) -> tuple[int, int, float]:
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

        return (deg_int, min_int, sec)

    if input_str.endswith("deg"):
        input_str = input_str.replace("deg", "")
        degrees = float(input_str)
        return _format_angular_units(degrees, 360, 60, 60)

    if input_str.endswith("grd"):
        input_str = input_str.replace("grd", "")
        gradians = float(input_str)
        return _format_angular_units(gradians, 400, 100, 100)

    print("Ungültige Eingabe. Geben Sie eine Zahl, gefolgt von 'deg' oder 'grd' ein.")
    return None


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
        fib_numbers.append(fib_numbers[-1] + fib_numbers[-2])

    return fib_numbers


"""
Anschließend soll jede Funktion (mit beliebigen Übergabewerten) zumindest ein
Mal aufgerufen sowie die Rückgabewerte über die Konsole ausgegeben werden.
"""

# Ensure that this file is run as a program before performing input/output, otherwise this
# would run as a side-effect of importing this file.
if __name__ == "__main__":
    print(">>>")
    print("Aufgabe 1:")

    # Repeat until the user enters a valid input
    while True:
        print("Geben Sie einen Winkel in Dezimalgrad ein:")
        angle_str = input()
        result = convert_angular_input(angle_str)
        if result is None:
            # Invalid input, try again
            continue
        else:
            (degrees, minutes, seconds) = result
            print(f"Grad: {degrees}°")
            print(f"Min: {minutes}'")
            print(f"Sek: {seconds:.3f}''")
            break

    print("")
    print("Aufgabe 2:")

    # Repeat until the user enters a valid input
    while True:
        print("Geben Sie die Anzahl der Elemente (mind. 2) der Fibonacci Reihe an:")
        n = int(input())
        if not n >= 2:
            # Invalid input, try again
            continue
        else:
            print("Output:", fibonacci(n))
            break
