from __future__ import annotations
import math

from Angles import Angle


class CartesianCoordinate:
    x: float
    y: float

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __add__(self, other: CartesianCoordinate) -> CartesianCoordinate:
        return CartesianCoordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other: CartesianCoordinate) -> CartesianCoordinate:
        return CartesianCoordinate(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> CartesianCoordinate:
        return CartesianCoordinate(self.x * scalar, self.y * scalar)

    def length(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def toPolar(self) -> PolarCoordinate:
        return PolarCoordinate(
            angle=Angle(rad=math.atan2(self.y, self.x)), r=self.length()
        )


class PolarCoordinate:
    rad: float
    r: float

    def __init__(self, angle: Angle, r: float) -> None:
        self.rad = angle.rad
        self.r = r

    def __str__(self) -> str:
        return f"({self.rad}, {self.r})"

    def rotate(self, angle: Angle) -> PolarCoordinate:
        self.rad += angle.rad
        return self

    def setAngle(self, angle: Angle) -> PolarCoordinate:
        self.rad = angle.rad
        return self

    def setDistance(self, distance: float) -> PolarCoordinate:
        self.r = distance
        return self

    def toCartesian(self) -> CartesianCoordinate:
        return CartesianCoordinate(
            x=self.r * math.cos(self.rad), y=self.r * math.sin(self.rad)
        )


class Segment:
    startCoord: CartesianCoordinate
    endCoord: CartesianCoordinate

    def __init__(
        self, startCoord: CartesianCoordinate, endCoord: CartesianCoordinate
    ) -> None:
        self.startCoord = startCoord
        self.endCoord = endCoord

    def __str__(self) -> str:
        return f"{self.startCoord} - {self.endCoord}"

    # Rotates the Segment around it's start point
    def rotate(self, angle: Angle) -> Segment:
        self.endCoord = (
            self.startCoord
            + (self.endCoord - self.startCoord).toPolar().rotate(angle).toCartesian()
        )
        return self

    def length(self) -> float:
        return (self.endCoord - self.startCoord).length()

    def setLength(self, length: float) -> Segment:
        self.endCoord = self.startCoord + (self.endCoord - self.startCoord) * (
            length / self.length()
        )
        return self
