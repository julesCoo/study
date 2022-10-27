from __future__ import annotations
from typing import Optional
from matplotlib import pyplot as plt
from lib.Algorithms import HA1
from lib.Point import Point
from lib.Line import Line


class Plot:
    min: Point
    max: Point

    def __init__(self, min: Point, max: Point):
        self.min = min
        self.max = max

        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect("equal")
        self.ax.set_xlim(min.y, max.y)
        self.ax.set_ylim(min.x, max.x)
        self.ax.grid()

        self.ax.set_xlabel("y")
        self.ax.set_ylabel("x")

    def add_point(self, p: Point, label: Optional[str] = None):
        self.ax.plot(p.y, p.x, "o")
        if label is not None:
            self.ax.annotate(label, (p.y, p.x))

    def add_line(self, line: Line):
        P0 = line.offset

        P1 = HA1(P0, line.angle, 1000)
        P2 = HA1(P0, line.angle, -1000)

        x = [P1.x, P2.x]
        y = [P1.y, P2.y]
        self.ax.plot(y, x)

    def add_circle(self, center: Point, radius: float):
        circle = plt.Circle((center.y, center.x), radius, fill=False)
        self.ax.add_artist(circle)

    def save(self, filename: str):
        self.fig.savefig(filename)
