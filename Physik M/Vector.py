from __future__ import annotations
from dataclasses import dataclass
import math


@dataclass
class Vec3:
    x: float
    y: float
    z: float

    def normalized(self):
        l = self.length()
        return Vec3(self.x / l, self.y / l, self.z / l)

    def length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def __add__(self, other: Vec3):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vec3):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float):
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def dot(self, other: Vec3):
        return self * other

    def cross(self, other: Vec3):
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def angleTo(self, other: Vec3):
        return math.acos(self.normalized() * other.normalized())
