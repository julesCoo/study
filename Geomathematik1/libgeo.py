from math import tau
import re

# Converts between various angle formats.
# Uses radians internally, since this is obviously the best format for computers.
class Angle:
    radians: float

    def __init__(self, rad: float):
        self.radians = rad

    def to_rad(self):
        return self.radians

    def to_deg(self):
        return 360 * (self.radians / tau)

    def to_deg_str(self, precision: int = 5):
        degrees = 360 * (self.radians / tau)
        is_negative = degrees < 0

        rest = abs(degrees)

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

        if is_negative:
            dd *= -1

        return f"{dd:02d}°{mm:02d}'{ss:02f}\""

    def to_gon(self):
        return 400 * (self.radians / tau)

    def to_gon_str(self, precision: int = 5):
        gradians = 400 * (self.radians / tau)
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

        return f"{dd:02d}°{mm:02d}'{ss:02f}\""

    @classmethod
    def from_rad(cls, radians: float):
        return cls(radians)

    @classmethod
    def from_deg(cls, degrees: float, minutes: float = 0, seconds: float = 0):
        is_negative = degrees < 0

        degrees = abs(degrees)
        degrees += minutes / 60
        degrees += seconds / (60 * 60)
        if is_negative:
            degrees *= -1

        rad = tau * degrees / 360
        return cls.from_rad(rad)

    @classmethod
    def from_gon(cls, dd: float, mm: float = 0, ss: float = 0):
        is_negative = dd < 0

        gons = abs(dd)
        gons += mm / 100
        gons += ss / (100 * 100)
        if is_negative:
            gons *= -1

        rad = tau * gons / 400
        return cls.from_rad(rad)

    @classmethod
    def from_gon_str(cls, gon_str: str):
        match = re.match(r"(-?\d+)°(\d+)'(\d+\.?\d*)\"?", gon_str)
        if match is None:
            raise ValueError("Invalid format. Should be dd°mm'ss\"")
        dd, mm, ss = match.groups()
        return cls.from_gon(float(dd), float(mm), float(ss))
