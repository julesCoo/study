from __future__ import annotations
import math


class Vec3:
    x: float
    y: float
    z: float

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"

    def __getitem__(self, index: int) -> float:
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        if index == 2:
            return self.z
        raise IndexError("index out of range")

    def __add__(self, other: Vec3) -> Vec3:
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vec3) -> Vec3:
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scale: float) -> Vec3:
        return Vec3(self.x * scale, self.y * scale, self.z * scale)

    def __rmul__(self, scale: float) -> Vec3:
        return self * scale

    def __truediv__(self, scale: float) -> Vec3:
        return Vec3(self.x / scale, self.y / scale, self.z / scale)

    def dot(self, other: Vec3) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vec3) -> Vec3:
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def length(self) -> float:
        return self.norm()

    def norm(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self) -> float:
        norm = self.norm()
        self.x /= norm
        self.y /= norm
        self.z /= norm
        return norm

    def normalized(self) -> Vec3:
        norm = self.norm()
        return Vec3(self.x / norm, self.y / norm, self.z / norm)

    def distance_to(self, other: Vec3) -> float:
        return math.sqrt(
            (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
        )

    def angle_between(self, other: Vec3) -> float:
        return math.acos(self.dot(other) / (self.norm() * other.norm()))
