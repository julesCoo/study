from __future__ import annotations

from lib.Point import Point


class Circle:
    center: Point
    radius: float

    def __init__(self, center: Point, radius: float):
        self.center = center
        self.radius = radius
