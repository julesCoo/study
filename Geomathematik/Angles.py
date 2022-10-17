from __future__ import annotations
import math
from typing import Optional


class Angle:
    rad: float = 0

    def __init__(
        self,
        rad: Optional[float] = None,
        deg: Optional[float] = None,
        gon: Optional[float] = None,
    ) -> None:
        if rad is not None:
            self.rad = rad

        if deg is not None:
            self.rad = deg * 2 * math.pi / 360

        if gon is not None:
            self.rad = gon * 2 * math.pi / 400

    def __str__(self) -> str:
        return f"{self.rad} rad"

    def __add__(self, other: Angle) -> Angle:
        return Angle(rad=self.rad + other.rad)

    def __sub(self, other: Angle) -> Angle:
        return Angle(rad=self.rad - other.rad)

    def __mul__(self, scalar: float) -> Angle:
        return Angle(rad=self.rad * scalar)

    def toDeg(self) -> float:
        return 360 * self.rad / 2 * math.pi

    def toGon(self) -> float:
        return 360 * self.rad / 2 * math.pi


def rad(rad: float) -> Angle:
    return Angle(rad=rad)


def deg(deg: float) -> Angle:
    return Angle(deg=deg)


def gon(gon: float) -> Angle:
    return Angle(gon=gon)
