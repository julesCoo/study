from __future__ import annotations
from typing import Optional
from Point import Point
from Angle import Angle


class Line:
    offset: Point
    angle: Angle

    def __init__(self, offset: Point, angle: Angle):
        self.offset = offset
        self.angle = angle

    @classmethod
    def from_points(cls, p1: Point, p2: Point) -> Line:
        return cls(p1, p1.oriented_angle_to(p2))

    def intersection(self, other: Line) -> Optional[Point]:
        if self.angle.rad == other.angle.rad:
            return None

        x0 = self.offset.x
        y0 = self.offset.y
        tan0 = self.angle.tan()

        x1 = other.offset.x
        y1 = other.offset.y
        tan1 = other.angle.tan()

        x = (y1 - y0 + tan0 * x0 - tan1 * x1) / (tan0 - tan1)
        y = tan0 * (x - x0) + y0
        return Point(x, y)
