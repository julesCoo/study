from typing import Union
from numpy import pi, sin, cos, sqrt, arctan2

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

    def __sub__(self, other):
        return YX(self.y - other.y, self.x - other.x)

    def to_polar(self):
        s = sqrt(self.y**2 + self.x**2)
        t = arctan2(self.y, self.x)
        return Polar(s, t)

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

    def polar_to(self, other: "YX"):
        return (other - self).to_polar()


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


def vws(p1: YX, p2: YX, t13: float, t23: float) -> YX:
    "Vorwärtsschnitt mit orientierten Richtungen"

    d12, t12 = p1.polar_to(p2)
    d13 = d12 * sin(t23 - t12) / sin(t23 - t13)
    return p1 + Polar(d13, t13)


# %%
"""Plotting"""
import matplotlib.pyplot as plt


# %%
