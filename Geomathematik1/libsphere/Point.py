from __future__ import annotations
from math import degrees, radians
from libsphere.Triangle import Triangle


class Point:
    phi: float
    lamda: float

    def __init__(self, phi: float, lamda: float):
        self.phi = phi
        self.lamda = lamda

    def __str__(self):
        return f"({degrees(self.phi):.4f}°, {degrees(self.lamda):.4f}°)"

    def __eq__(self, other: Point):
        return abs(self.phi - other.phi) < 1e-3 and abs(self.lamda - other.lamda) < 1e-3


def HA1(
    point: Point,
    angle: float,
    distance: float,
) -> tuple[Point, float]:
    triangle = Triangle.sws(
        a=radians(90) - point.phi,
        b=distance,
        gamma=angle,
    )

    point2 = Point(
        phi=radians(90) - triangle.c,
        lamda=triangle.beta + point.lamda,
    )
    angle_back = radians(360) - triangle.alpha
    return point2, angle_back


def HA2(
    point1: Point,
    point2: Point,
) -> tuple[float, float]:
    triangle = Triangle.sws(
        a=radians(90) - point1.phi,
        b=radians(90) - point2.phi,
        gamma=point2.lamda - point1.lamda,
    )

    dist = triangle.c
    angle = triangle.beta

    return dist, angle
