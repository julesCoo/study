from __future__ import annotations
import math
from lib2d.Algorithms import HA1
from lib2d.Line import Line
from lib2d.Point import Point


class Circle:
    center: Point
    radius: float

    def __init__(self, center: Point, radius: float):
        self.center = center
        self.radius = radius

    def intersect_line(self, line: Line) -> tuple[Point, Point]:
        # Translate coordinates so that the circle is centered at the origin
        # We later translate the result back
        o = line.offset - self.center
        d = line.direction_vec()

        # From combining the line equation with the circle equation:
        # x = o.x + d.x * t
        # y = o.y + d.y * t
        # x^2 + y^2 = r^2
        ph = d.x * o.x + d.y * o.y
        q = o.x**2 + o.y**2 - self.radius**2

        t0 = -ph + math.sqrt(ph**2 - q)
        t1 = -ph - math.sqrt(ph**2 - q)

        p1 = o + d * t0 + self.center
        p2 = o + d * t1 + self.center

        return p1, p2
