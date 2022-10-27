from Coordinates import Segment
from Coordinates import CartesianCoordinate
import matplotlib.pyplot as plt


class Plot:
    def __init__(self, x_range: tuple[float, float], y_range: tuple[float, float]):
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect("equal")
        self.ax.set_xlim(x_range[0], x_range[1])
        self.ax.set_ylim(y_range[0], y_range[1])
        self.ax.grid()

    def add_known_point(self, p: CartesianCoordinate):
        self.ax.plot(p.y, p.x, "^")

    def add_measured_point(self, p: CartesianCoordinate):
        self.ax.plot(p.y, p.x, ".")

    def add_segment(self, s: Segment):
        self.ax.plot([s.start.y, s.end.y], [s.start.x, s.end.x])

    def show(self):
        plt.show()

    def save(self, filename: str):
        self.fig.savefig(filename)
