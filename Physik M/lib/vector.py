from __future__ import annotations
import math


def fmt_number(num: float) -> str:
    """Format a number for printing."""
    return f"{num:.5e}".replace("+", "")


class Vec2:
    x: float
    y: float

    def __init__(
        self,
        x: float,
        y: float,
    ):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({fmt_number(self.x)}, {fmt_number(self.y)})"

    def normalize(self) -> float:
        norm = self.length()
        self.x /= norm
        self.y /= norm
        return norm

    def normalized(self) -> Vec2:
        l = self.length()
        return Vec2(self.x / l, self.y / l)

    def length(self) -> float:
        return math.sqrt(
            self.x**2 + self.y**2,
        )

    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(
            self.x + other.x,
            self.y + other.y,
        )

    def __sub__(self, other: Vec2) -> Vec2:
        return Vec2(
            self.x - other.x,
            self.y - other.y,
        )

    def __mul__(self, scalar: float) -> Vec2:
        return Vec2(
            self.x * scalar,
            self.y * scalar,
        )

    def __div__(self, scalar: float) -> Vec2:
        return self * (1 / scalar)

    def __neg__(self) -> Vec2:
        return self * -1

    def dot(self, other: Vec2) -> float:
        return self.x * other.x + self.y * other.y

    def __matmul__(self, other: Vec2) -> float:
        return self.dot(other)

    def angleTo(self, other: Vec2) -> float:
        return math.acos(self.normalized() * other.normalized())


class Vec3:
    x: float
    y: float
    z: float

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"({fmt_number(self.x)}, {fmt_number(self.y)}, {fmt_number(self.z)})"

    def normalize(self) -> float:
        norm = self.length()
        self.x /= norm
        self.y /= norm
        self.z /= norm
        return norm

    def normalized(self) -> Vec3:
        l = self.length()
        return Vec3(
            self.x / l,
            self.y / l,
            self.z / l,
        )

    def length(self) -> float:
        return math.sqrt(
            self.x**2 + self.y**2 + self.z**2,
        )

    def __add__(self, other: Vec3) -> Vec3:
        return Vec3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )

    def __sub__(self, other: Vec3) -> Vec3:
        return Vec3(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
        )

    def __mul__(self, scalar: float) -> Vec3:
        return Vec3(
            self.x * scalar,
            self.y * scalar,
            self.z * scalar,
        )

    def __div__(self, scalar: float) -> Vec3:
        return self * (1 / scalar)

    def __neg__(self) -> Vec3:
        return self * -1

    def dot(self, other: Vec3) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __matmul__(self, other: Vec3) -> float:
        return self.dot(other)

    def cross(self, other: Vec3) -> Vec3:
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def angleTo(self, other: Vec3) -> float:
        return math.acos(self.normalized() * other.normalized())
