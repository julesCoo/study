# %%
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from matplotlib import cm
import mpl_toolkits.mplot3d as mplot3d
import meshio
import numpy as np
from copy import deepcopy
from pathlib import Path
from datetime import datetime, timedelta
from math import pi, sin, cos

# %%

"""
First we define some classes to represent the measurements we will be working with.

Each measurement is taken at a specific time, which is called an Epoch.

Measurements of the Tachymeter and Laserscanner describe polar coordinates, and will are
stored as `PolarEpoch` objects.

Within a cartesic coordinate system, positions are described as `PositionEpoch` objects.
"""


class Epoch:
    """
    Creates the class Epoch to manage timestamps
    """

    _time: datetime

    def __init__(self, time: datetime):
        """
        Constructor: Sets time (datetime)
        :param time: Timestamp of data
        """
        self.time = time

    @property
    def time(self) -> datetime:
        return self._time

    @time.setter
    def time(self, value: datetime) -> None:
        if not isinstance(value, datetime):
            raise TypeError(f"Expected datetime, got {type(value)}")
        self._time = value

    def __eq__(self, other: "Epoch") -> bool:
        return self.time == other.time

    def __ne__(self, other: "Epoch") -> bool:
        return self.time != other.time

    def __lt__(self, other: "Epoch") -> bool:
        return self.time < other.time

    def __le__(self, other: "Epoch") -> bool:
        return self.time <= other.time

    def __gt__(self, other: "Epoch") -> bool:
        return self.time > other.time

    def __ge__(self, other: "Epoch") -> bool:
        return self.time >= other.time


class PositionEpoch(Epoch):
    """
    Creates class to store Points in cartesian coordinates
    """

    _x: float
    _y: float
    _z: float

    def __init__(self, time: datetime, x: float = 0, y: float = 0, z: float = 0):
        """
        Constructor: Overwrites time and sets Coordinates
        :param time: Timestamp of data (datetime)
        :param x: x Coordinate (float)
        :param y: y Coordinate (float)
        :param z: z Coordinate (float)
        """
        super().__init__(time)
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f"Position({self.time}, {self.x}, {self.y}, {self.z})"

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def z(self) -> float:
        return self._z

    @x.setter
    def x(self, value: float) -> None:
        if not isinstance(value, float):
            raise TypeError(f"Expected float, got {type(value)}")
        self._x = value

    @y.setter
    def y(self, value: float) -> None:
        if not isinstance(value, float):
            raise TypeError(f"Expected float, got {type(value)}")
        self._y = value

    @z.setter
    def z(self, value: float) -> None:
        if not isinstance(value, float):
            raise TypeError(f"Expected float, got {type(value)}")
        self._z = value

    def __add__(self, other: "PositionEpoch") -> "PositionEpoch":
        if self.time != other.time:
            raise ValueError("Epochs must have the same time")
        return PositionEpoch(
            self.time,
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )


class PolarEpoch(Epoch):
    """
    Creates class to store Points with 2 angles (zenit, azimuth) and distance
    """

    _distance: float
    _azimuth: float
    _zenith: float

    def __init__(
        self, time: datetime, azimuth: float = 0, distance: float = 0, zenith: float = 0
    ):
        """
        Constructor: Overwrites time and sets distance, zenit and azimut angles
        :param time: Timestamp of data (datetime)
        :param azimuth: azimuth angle (float)
        :param distance: distance (float)
        :param zenit: zenit angle (float)
        """
        super().__init__(time)
        self.distance = distance
        self.azimuth = azimuth
        self.zenith = zenith

    def __repr__(self) -> str:
        return f"Polar({self.time}, {self.azimuth}, {self.distance}, {self.zenith})"

    @property
    def distance(self) -> float:
        return self._distance

    @property
    def azimuth(self) -> float:
        return self._azimuth

    @property
    def zenith(self) -> float:
        return self._zenith

    @distance.setter
    def distance(self, value: float) -> None:
        if not isinstance(value, float):
            raise TypeError(f"Expected float, got {type(value)}")
        if value < 0:
            raise ValueError(f"Distance must be positive, got {value}")
        self._distance = value

    @azimuth.setter
    def azimuth(self, value: float) -> None:
        if not isinstance(value, float):
            raise TypeError(f"Expected float, got {type(value)}")
        if value < -pi or value > pi:
            raise ValueError(f"Azimuth must be between -pi and pi radians, got {value}")
        self._azimuth = value

    @zenith.setter
    def zenith(self, value: float) -> None:
        if not isinstance(value, float):
            raise TypeError(f"Expected float, got {type(value)}")
        if value < 0 or value > pi:
            raise ValueError(f"Zenith must be between 0 and pi radians, got {value}")
        self._zenith = value

    def to_position(self) -> PositionEpoch:
        """
        Converts polar coordinates to cartesian coordinates
        """
        x = self.distance * sin(self.zenith) * cos(self.azimuth)
        y = self.distance * sin(self.zenith) * sin(self.azimuth)
        z = self.distance * cos(self.zenith)
        return PositionEpoch(self.time, x, y, z)


# %%
"""
Now the data from the files can be read in.
There are two files containing polar epochs.
"""

# Time values are given as offset seconds since 2018-03-13 15:10:00
start_date = datetime(2018, 3, 13, 15, 10, 0)


def load_polar_epochs(filename: str) -> list[PolarEpoch]:
    """
    Reads .txt files and returns them in a list consisting of instances of the class Polar Epoch.
    :param filename: Name of the file to be imported
    """
    polar_epochs = []
    # File is opend via "read"
    with open(filename, "r") as f:
        for line in f:
            time, distance, zenith, azimuth = line.split(" ")
            polar_epochs.append(
                PolarEpoch(
                    time=start_date + timedelta(seconds=float(time)),
                    distance=float(distance),
                    zenith=float(zenith),
                    azimuth=float(azimuth),
                )
            )
    return polar_epochs


# The two given data sets are read in
tachy_measurements = load_polar_epochs(Path(__file__).parent / "obsTachy.txt")
laser_measurements = load_polar_epochs(Path(__file__).parent / "obsDrone.txt")

# %%
"""
Before working with the data, it needs to be sorted by time.

For this, we write a custom bubblesort function and compare its performance with
the built-in `Array.sort` function.

To measure the performance, a custom Timer class is created.
"""


def bubble_sort(arr: list) -> list:
    """
    Sorts a list in ascending order
    :param arr: List to be sorted
    """
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


class Timer:
    """
    Creates a class for measuring the time of a process
    """

    _name: str
    _start: datetime

    def __init__(self, name="Unnamed Timer") -> None:
        """
        Construktor
        :param name: Custom name of the Timer
        """
        self._name = name

    def __enter__(self):
        # Starts the timer
        self._start = datetime.now()

    def __exit__(self, *args):
        # Stops the timer and prints result
        interval = datetime.now() - self._start
        print(f"[{self._name}] Time elapsed: {interval.total_seconds()} s")


# Copy the arrays before sorting, so the original data won´t be modified
arr_copy = deepcopy(tachy_measurements)
with Timer("bubble_sort"):
    bubble_sort(arr_copy)

arr_copy = deepcopy(tachy_measurements)
with Timer("list.sort"):
    arr_copy.sort()

# The timer shows that the built-in sort function is much faster than our custom
# bubblesort function, so it is used to sort the observations.
tachy_measurements.sort()
laser_measurements.sort()

# %%
"""
Now that the observations are sorted, we can begin to combine them into 3d coordinates.
The drone is moving in a trajectory tracked by the tachymeter, and is performing many
laser scanner measurements while in flight.

At each drone position, we expect to find multiple laser scanner measurements.
Since both lists are sorted by time, we can iterate through the lists in parallel and match
the measurements according to their epoch time.

This search has a complexity of O(n) (but pre-sorting has O(n log n)).
"""

drone_positions: list[PositionEpoch] = []
for polar in tachy_measurements:
    # The tachymeter position is constant throughout the experiment.
    # But we have to set the correct time for each position epoch.
    tachy_position = PositionEpoch(time=polar.time, x=-51.28, y=-4.373, z=1.34)
    # We can then add the relative position to get its absolute position.
    drone_position = tachy_position + polar.to_position()
    drone_positions.append(drone_position)

ground_positions: list[PositionEpoch] = []

# For each drone_position, there might be multiple laser measurements.
# But since both lists are sorted, we just have to seek through both list.
drone_index = 0
laser_index = 0

while drone_index < len(drone_positions) and laser_index < len(laser_measurements):
    drone_position = drone_positions[drone_index]
    laser_polar = laser_measurements[laser_index]

    # If both timestamps match, we can combine them into one ground position measurement.
    if drone_position.time == laser_polar.time:
        ground_pos = drone_position + laser_polar.to_position()
        ground_positions.append(ground_pos)

        # Then we can look at the next laser measurement.
        laser_index += 1

    # If the laser measurement is too early, we have to look at the next drone position.
    elif laser_polar.time < drone_position.time:
        laser_index += 1

    # If the laser measurement is too late, we have to look at the next drone position.
    else:
        drone_index += 1

# %%
"""
The `ground_positions` list is a point cloud, which limits the options we have to visualize
and analyze it. Therefore, we now create a heightmap from it, by pooling all measurements in
50x50 cm grid cells and calculating the average height of all measurements in each cell.
"""


# Extract x and y positions of the ground positions
x = [p.x for p in ground_positions]
y = [p.y for p in ground_positions]
x_min, x_max = min(x), max(x)
y_min, y_max = min(y), max(y)

grid_size = 0.5

# Create an xy grid with 50cm resolution
xs_grid = np.arange(x_min, x_max, grid_size)
yy_grid = np.arange(y_min, y_max, grid_size)
X, Y = np.meshgrid(xs_grid, yy_grid)

# For each grid cell, store the sum of the heights and the count of measurements
Z = np.zeros_like(X)
Z_count = np.zeros_like(X)


def pos_to_grid_index(p):
    x_index = int((p.x - x_min) / grid_size)
    y_index = int((p.y - y_min) / grid_size)
    return x_index, y_index


for drone_pos in ground_positions:
    # Determine the grid cell for the current position
    xi, yi = pos_to_grid_index(drone_pos)

    # Add the height to the grid point
    Z[yi, xi] += drone_pos.z
    Z_count[yi, xi] += 1


# Calculate the average height for each cell
# prevent division by zero first, some cells might not have any measurements
Z_count[Z_count == 0] = 1
Z /= Z_count


def grid_index_to_pos(xi, yi):
    x = x_min + xi * grid_size
    y = y_min + yi * grid_size
    if yi < 0 or xi < 0 or yi >= Z.shape[0] or xi >= Z.shape[1]:
        z = 0.0
    else:
        z = Z[yi, xi]
    return PositionEpoch(start_date, x, y, z)


# %%
"""
Preparations for visualizations. We will create a series of 3d plots,
which have a common base configuration.
"""


class BasePlot:
    fig: plt.Figure
    ax: plt.Axes

    def __init__(self, name: str) -> None:
        self.name = name
        pass

    def __enter__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(
            projection="3d",
            elev=15,
            azim=200,
            # we have some issues with the contour plot overlapping the wireframe,
            # so we disable the zorder computation
            computed_zorder=False,
            xlabel="x [m]",
            ylabel="y [m]",
            zlabel="z [m]",
            xlim=[-40, 40],
            ylim=[-40, 40],
            zlim=[0, 50],
        )
        # make the grid lines less prominent
        plt.rcParams["grid.color"] = (0.5, 0.5, 0.5, 0.01)

        # ensure equal aspect ratio to not deform the model
        self.ax.set_aspect("equal")

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        plt.savefig(f"{self.name}.png", dpi=400)
        print(f"Saved {self.name}.png")
        plt.show()
        plt.close(self.fig)


# %%
"""
3D model of the raw data with surface smoothing:
"""

with BasePlot("Surface") as plot:
    # The rstride and cstride parameters are used to show the whole surface.
    plot.ax.plot_surface(
        X,
        Y,
        Z,
        cmap=cm.coolwarm,
        rstride=1,
        cstride=1,
    )
    plot.ax.plot_wireframe(
        X,
        Y,
        Z,
        color="white",
        alpha=0.02,
        cstride=1,
        rstride=1,
    )

# %%
"""
3D model as point cloud without gridding
"""

with BasePlot("PointCloud") as plot:
    plot.ax.scatter(
        [p.x for p in ground_positions],
        [p.y for p in ground_positions],
        [p.z for p in ground_positions],
        c="red",
        s=0.0001,
        alpha=1.0,
    )

# %%
"""
3D model with extended features:
"""

with BasePlot("FeaturePlot") as plot:
    # Draw a contour plot of the heightmap at the xy plane, with colors
    # representing the height. Also add a colorbar.
    cnt = plot.ax.contourf(
        X,
        Y,
        Z,
        cmap="inferno",
        zdir="z",
        offset=0,
        alpha=0.8,
    )
    plot.fig.colorbar(cnt, ax=plot.ax, shrink=0.5, label="z [m]")

    # Draw a (ghostly) wireframe of the building on top of the contour
    plot.ax.plot_wireframe(
        X,
        Y,
        Z,
        color="black",
        alpha=0.05,
        cstride=1,
        rstride=1,
    )

    # Draw the flight path of the drone as dotted line
    plot.ax.plot(
        [p.x for p in drone_positions],
        [p.y for p in drone_positions],
        [p.z for p in drone_positions],
        color="gray",
        dashes=[10, 5],
        linewidth=1,
        alpha=0.3,
    )

    # Draw a small sphere at the drone position
    drone_index = 290
    drone_pos = drone_positions[drone_index]
    plot.ax.scatter(
        drone_pos.x,
        drone_pos.y,
        drone_pos.z,
        color="black",
        s=10,
    )

    # Find the laser scanner measurements from the drone at this position
    drone_time = drone_positions[drone_index].time
    for p in ground_positions:
        if p.time == drone_time:
            # Draw laser lines originating from the drone towards the ground
            plot.ax.plot(
                [drone_pos.x, p.x],
                [drone_pos.y, p.y],
                [drone_pos.z, p.z],
                color="red",
                alpha=0.0075,
            )
            # Then highlight the measured ground positions with red dots
            plot.ax.scatter(
                p.x,
                p.y,
                p.z,
                color="red",
                s=0.1,
                alpha=0.5,
            )

    # Draw a small tachymeter from 5 points :)
    tachymeter_center = PositionEpoch(start_date, x=-51.28, y=-4.373, z=1.34)
    tachymeter_head = tachymeter_center + PositionEpoch(start_date, 0.0, 0.0, 0.5)
    tachymeter_leg1 = tachymeter_center + PositionEpoch(start_date, -1.0, 0.0, -1.5)
    tachymeter_leg2 = tachymeter_center + PositionEpoch(start_date, 0.0, 1.0, -1.5)
    tachymeter_leg3 = tachymeter_center + PositionEpoch(start_date, 0.7, -0.7, -1.5)
    for pos in [tachymeter_leg1, tachymeter_leg2, tachymeter_leg3, tachymeter_head]:
        plot.ax.plot(
            [tachymeter_center.x, pos.x],
            [tachymeter_center.y, pos.y],
            [tachymeter_center.z, pos.z],
            color="black",
        )

    # draw a dotted line from the tachymeter to a drone position
    plot.ax.plot(
        [drone_pos.x, tachymeter_head.x],
        [drone_pos.y, tachymeter_head.y],
        [drone_pos.z, tachymeter_head.z],
        color="red",
        linewidth=1.0,
        dashes=[2, 4],
    )

# %%
"""
Export of the 3D model as STL for 3D-Printing
"""
# Creating the surface plot with triangulation (this is the slow part)
triang = mtri.Triangulation(X.ravel(), Y.ravel())

# Export to STL with meshio
mesh = meshio.Mesh(
    points=np.c_[X.ravel(), Y.ravel(), Z.ravel()],
    cells=[("triangle", triang.triangles)],
)
meshio.write("Steyrergasse_30.stl", mesh, file_format="stl")

# Plot the surface to check if it looks good
with BasePlot("STL_Model") as plot:
    plot.ax.plot_trisurf(triang, Z.ravel(), cmap="coolwarm")

# %%
