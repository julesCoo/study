from __future__ import annotations
import math

from lib.Angle import Angle


class Point:
    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x:.4f}, {self.y:.4f})"

    def distance_to(self, other: Point) -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def oriented_angle_to(self, other: Point) -> Angle:
        return Angle(rad=math.atan2(other.y - self.y, other.x - self.x))
