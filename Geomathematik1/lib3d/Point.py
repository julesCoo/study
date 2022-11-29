from __future__ import annotations
import math


class Point:
    x: float
    y: float
    z: float

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"

    def distance_to(self, other: Point) -> float:
        return math.sqrt(
            (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
        )

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scale: float) -> Point:
        return Point(self.x * scale, self.y * scale, self.z * scale)

    def dot(self, other: Point) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Point) -> Point:
        return Point(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def normalize(self):
        length = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        self.x /= length
        self.y /= length
        self.z /= length
