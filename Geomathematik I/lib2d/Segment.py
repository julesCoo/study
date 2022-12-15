from __future__ import annotations
from lib2d.Algorithms import HA1
from lib.Angle import gon
from lib2d.Line import Line
from lib2d.Point import Point


class Segment:
    p1: Point
    p2: Point

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    @classmethod
    def from_points(cls, p1: Point, p2: Point) -> Segment:
        return cls(p1, p2)

    def length(self) -> float:
        return self.p1.distance_to(self.p2)

    def angle(self) -> float:
        return self.p1.oriented_angle_to(self.p2)

    def center(self) -> Point:
        return HA1(self.p1, self.length() / 2, self.angle())

    def perpendicular_bisector(self) -> Line:
        return Line(self.center(), self.angle() + gon(100))
