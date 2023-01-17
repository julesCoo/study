from math import tau
import re


def clamp_rad(a):
    while a < 0:
        a += tau
    while a >= tau:
        a -= tau
    return a


# Converts radians to gradians (gon).
# Similar to math.degrees().
def gradians(radians: float) -> float:
    return 400 * (radians / tau)


# Converts gradians (gon) to radians (rad).
# Input can be given as a single value or with minutes and seconds.
def from_gon(gradians: float, minutes: float = 0, seconds: float = 0) -> float:
    is_negative = gradians < 0

    gons = abs(gradians)
    gons += minutes / 100
    gons += seconds / (100 * 100)
    if is_negative:
        gons *= -1

    return tau * gons / 400


# Converts degrees (deg) to radians (rad).
# Input can be given as a single value or with minutes and seconds.
def from_deg(degrees: float, minutes: float = 0, seconds: float = 0) -> float:
    is_negative = degrees < 0

    degrees = abs(degrees)
    degrees += minutes / 60
    degrees += seconds / (60 * 60)
    if is_negative:
        degrees *= -1

    return tau * degrees / 360


# Converts an angle (given in radians) to a string.
# Result is formatted as a single value with the given precision.
def fmt_deg(radians: float, precision: int = 3) -> str:
    deg = radians / tau * 360
    return f"{deg:.{precision}f}°"


# Converts an angle (given in radians) to a string.
# Result is formatted as dd°mm'ss".
def fmt_deg_str(radians: float, precision: int = 3) -> str:
    is_negative = radians < 0

    rest = abs(radians / tau * 360)

    dd = int(rest)
    rest -= dd
    rest *= 60

    mm = int(rest)
    rest -= mm
    rest *= 60

    ss = round(rest, precision)
    if ss == 60:
        ss = 0
        mm += 1
        if mm == 60:
            mm = 0
            dd += 1

    sgn = ""
    if is_negative:
        sgn = "-"

    return f"{sgn}{dd:02d}°{mm:02d}'{ss:02.{precision}f}\""


# Parses a string formatted as dd°mm'ss" and returns the corresponding angle in radians.
def parse_deg_str(deg_str: str) -> float:
    match = re.match(r"(-?\d+)°(\d+)'(\d+\.?\d*)\"?", deg_str)
    if match is None:
        raise ValueError("Invalid format. Should be dd°mm'ss\"")
    dd, mm, ss = match.groups()
    return from_deg(float(dd), float(mm), float(ss))


# Converts an angle (given in radians) to a string.
# Result is formatted as a single value with the given precision.
def fmt_gon(radians: float, precision: int = 3):
    gon = radians / tau * 400
    return f"{gon:.{precision}f}g"


# Converts an angle (given in radians) to a string.
# Result is formatted as ddgmm'ss".
def fmt_gon_str(radians: float, precision: int = 3) -> str:
    gradians = radians / tau * 400
    is_negative = gradians < 0

    rest = abs(gradians)

    dd = int(rest)
    rest -= dd
    rest *= 100

    mm = int(rest)
    rest -= mm
    rest *= 100

    ss = round(rest, precision)
    if ss == 100:
        ss = 0
        mm += 1
        if mm == 100:
            mm = 0
            dd += 1

    if is_negative:
        dd *= -1

    return f"{dd:02d}g{mm:02d}'{ss:02f}\""


# Parses a string formatted as ddgmm'ss" and returns the corresponding angle in radians.
def parse_gon_str(gon_str: str) -> float:
    match = re.match(r"(-?\d+)g(\d+)'(\d+\.?\d*)\"?", gon_str)
    if match is None:
        raise ValueError("Invalid format. Should be dd°mm'ss\"")
    dd, mm, ss = match.groups()
    return from_gon(float(dd), float(mm), float(ss))
