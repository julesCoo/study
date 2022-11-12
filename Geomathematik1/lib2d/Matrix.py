from __future__ import annotations

from lib2d.Point import Point
from lib.Angle import Angle

"""
M = | xx xy |
    | yx yy |
"""


class Matrix:
    xx: float
    xy: float
    yx: float
    yy: float

    def __init__(self, xx: float, xy: float, yx: float, yy: float):
        self.xx = xx
        self.xy = xy
        self.yx = yx
        self.yy = yy

    @classmethod
    def identity(cls) -> Matrix:
        return cls(1, 0, 0, 1)

    @classmethod
    def rotation(cls, angle: Angle) -> Matrix:
        return cls(
            angle.cos(),
            -angle.sin(),
            angle.sin(),
            angle.cos(),
        )

    def __mul__(self, point: Point) -> Point:
        return Point(
            self.xx * point.x + self.xy * point.y,
            self.yx * point.x + self.yy * point.y,
        )
