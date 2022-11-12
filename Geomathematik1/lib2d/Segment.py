from __future__ import annotations
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
