from __future__ import annotations
from typing import Optional
from lib.Algorithms import Vorwärtsschnitt_Richtung
from lib.Point import Point
from lib.Angle import Angle


class Line:
    offset: Point
    angle: Angle

    def __init__(self, offset: Point, angle: Angle):
        self.offset = offset
        self.angle = angle

    @classmethod
    def from_points(cls, p1: Point, p2: Point) -> Line:
        return cls(p1, p1.oriented_angle_to(p2))

    def direction_vec(self) -> Point:
        return Point(self.angle.cos(), self.angle.sin())

    def intersection(self, other: Line) -> Optional[Point]:
        if self.angle.rad == other.angle.rad:
            return None

        return Vorwärtsschnitt_Richtung(
            self.offset, other.offset, self.angle, other.angle
        )
