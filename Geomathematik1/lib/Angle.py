from __future__ import annotations
import math

# Creates an Angle from Radians
def rad(rad: float) -> Angle:
    return Angle(rad)


# Creates an Angle from Gon
def gon(gon: float) -> Angle:
    return Angle(gon * math.tau / 400)


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
        return f"{gon:.4f}g"

    def reverse(self) -> Angle:
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
