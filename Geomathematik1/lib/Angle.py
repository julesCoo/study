from __future__ import annotations
import math

# Creates an Angle from Radians
def rad(rad: float) -> Angle:
    return Angle(rad)


# Creates an Angle from Gon
def gon(gon: float) -> Angle:
    return Angle(gon * math.tau / 400)


# Encapsulates an Angle.
# Internally stored in radians, but can be created from and converted to Gon.
# The constructor automatically normalizes the angle to the range [0, 2pi).
class Angle:
    rad: float

    def __init__(self, rad: float):
        while rad < 0:
            rad += math.tau
        while rad > math.tau:
            rad -= math.tau
        self.rad = rad

    def __str__(self) -> str:
        gon = self.rad * 400 / math.tau
        return f"{gon:.3f} gon"

    # Returns the angle pointing in the opposite direction
    def flip(self) -> Angle:
        return Angle(self.rad + math.pi)

    def __add__(self, other: Angle) -> Angle:
        return Angle(self.rad + other.rad)

    def __sub__(self, other: Angle) -> Angle:
        return Angle(self.rad - other.rad)

    def sin(self) -> float:
        return math.sin(self.rad)

    def cos(self) -> float:
        return math.cos(self.rad)

    def tan(self) -> float:
        return math.tan(self.rad)
