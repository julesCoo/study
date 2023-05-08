from typing import Tuple, Union
from numpy import pi, sin, cos, sqrt, arctan2, linalg, arccos, arctan

# %%
"""Angles"""


# Converts gradians to radians
def gon(gon: float) -> float:
    return gon * pi / 200


# Converts radians to gradians
def to_gon(rad: float) -> float:
    return rad * 200 / pi


#  Converts milligradians to radians
def mgon(gon: float) -> float:
    return gon * pi / 2000


def to_mgon(rad: float) -> float:
    return rad * 2000 / pi


# %%
"""Distances"""


# Converts meters to meters
def m(val: float) -> float:
    return val


def mm(val: float) -> float:
    return val / 1000


def cm(val: float) -> float:
    return val / 100


# %%
"""Coordinates"""


class YX:
    y: float
    x: float

    def __init__(self, y: float, x: float):
        self.y = y
        self.x = x

    def __repr__(self) -> str:
        return f"YX({self.y}, {self.x})"

    def __iter__(self):
        return iter([self.y, self.x])

    def __add__(self, other: Union["YX", "Polar"]):
        if isinstance(other, Polar):
            other = other.to_yx()
        return YX(self.y + other.y, self.x + other.x)

    def __sub__(self, other) -> "YX":
        return YX(self.y - other.y, self.x - other.x)

    def __mul__(self, other: float) -> "YX":
        return YX(self.y * other, self.x * other)

    def __rmul__(self, other: float) -> "YX":
        return self * other

    def __truediv__(self, other: float) -> "YX":
        return YX(self.y / other, self.x / other)

    def __neg__(self) -> "YX":
        return YX(-self.y, -self.x)

    def length(self) -> float:
        return sqrt(self.y**2 + self.x**2)

    def normalize(self) -> "YX":
        return self / self.length()

    def rotate(self, angle: float) -> "YX":
        return YX(
            -self.x * sin(angle) + self.y * cos(angle),
            self.x * cos(angle) + self.y * sin(angle),
        )

    def to_polar(self):
        s = sqrt(self.y**2 + self.x**2)
        t = arctan2(self.y, self.x)
        return Polar(s, t)

    def polar_to(self, other: "YX"):
        return (other - self).to_polar()

    def plot(self, label="", **kwargs):
        if "marker" not in kwargs:
            kwargs["marker"] = "^"
        if "color" not in kwargs:
            kwargs["color"] = "black"

        plt.scatter(self.y, self.x, **kwargs)
        if label:
            plt.text(self.y, self.x, label)

    def plot_to(self, other: "YX", **kwargs):
        if "color" not in kwargs:
            kwargs["color"] = "black"

        plt.plot([self.y, other.y], [self.x, other.x], **kwargs)


class Polar:
    d: float
    t: float

    def __init__(self, d: float, t: float):
        self.d = d
        self.t = t

    def __repr__(self) -> str:
        return f"Polar({self.d}, {self.t})"

    def to_yx(self):
        y = self.d * sin(self.t)
        x = self.d * cos(self.t)
        return YX(y, x)

    def __iter__(self):
        return iter([self.d, self.t])


# %%
"""Coordinate Calculations"""


def Halbwinkelsatz(
    a: float,
    b: float,
    c: float,
):
    s = (a + b + c) / 2
    alpha = 2 * arctan(sqrt((s - b) * (s - c) / (s * (s - a))))
    beta = 2 * arctan(sqrt((s - c) * (s - a) / (s * (s - b))))
    gamma = 2 * arctan(sqrt((s - a) * (s - b) / (s * (s - c))))
    return alpha, beta, gamma


def vws(p1: YX, p2: YX, t13: float, t23: float) -> YX:
    "Vorwärtsschnitt mit orientierten Richtungen"

    s12, t12 = p1.polar_to(p2)
    s13 = s12 * sin(t23 - t12) / sin(t23 - t13)
    return p1 + Polar(s13, t13)


def bgs(p1: YX, p2: YX, s13: float, s23: float) -> YX:
    "Bogenschnitt"

    s12, t12 = p1.polar_to(p2)
    alpha, _, _ = Halbwinkelsatz(s23, s13, s12)
    t13 = t12 + alpha
    return p1 + Polar(s13, t13)


class CoordinateTransform:
    "Transforms coordinates from one coordinate system (A) to another (B)"

    scale: float
    rotation: float
    translation: YX

    def __init__(
        self,
        scale: float = 1,
        rotation: float = 0,
        translation: YX = YX(0, 0),
    ):
        self.scale = scale
        self.rotation = rotation
        self.translation = translation

    def __repr__(self) -> str:
        return f"CoordinateTransform(scale={self.scale}, rotate={to_gon(self.rotation)} gon, translate={self.translation})"

    def transform(self, point: YX) -> YX:
        return (point * self.scale).rotate(self.rotation) + self.translation

    @classmethod
    def helmert(
        cls,
        from_points: Tuple[YX, YX],
        to_points: Tuple[YX, YX],
    ) -> "CoordinateTransform":
        y1, x1 = from_points[0]
        y2, x2 = from_points[1]

        y1_, x1_ = to_points[0]
        y2_, x2_ = to_points[1]

        a, b, c, d = linalg.lstsq(
            [
                [x1, y1, 1, 0],
                [x2, y2, 1, 0],
                [y1, -x1, 0, 1],
                [y2, -x2, 0, 1],
            ],
            [
                x1_,
                x2_,
                y1_,
                y2_,
            ],
            rcond=None,
        )[0]

        return CoordinateTransform(
            scale=sqrt(a**2 + b**2),
            rotation=arctan2(b, a),
            translation=YX(d, c),
        )


# %%
"""Plotting"""
import matplotlib.pyplot as plt


# %%
