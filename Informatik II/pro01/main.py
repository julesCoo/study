# %%
"""
First we define some classes to represent the measurements we will be working with.

Each measurement is taken at a specific time, which is called an Epoch.

Measurements of the Tachymeter and Laserscanner describe polar coordinates, and will are
stored as `PolarEpoch` objects.

Within a cartesic coordinate system, positions are described as `PositionEpoch` objects.
"""

from datetime import datetime, timedelta
from math import pi, sin, cos


class Epoch:
    _time: datetime

    def __init__(self, time: datetime):
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
    _x: float
    _y: float
    _z: float

    def __init__(self, time: datetime, x: float = 0, y: float = 0, z: float = 0):
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
    _distance: float
    _azimuth: float
    _zenith: float

    def __init__(
        self, time: datetime, azimuth: float = 0, distance: float = 0, zenith: float = 0
    ):
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
        """Converts polar coordinates to cartesian coordinates"""
        x = self.distance * sin(self.zenith) * cos(self.azimuth)
        y = self.distance * sin(self.zenith) * sin(self.azimuth)
        z = self.distance * cos(self.zenith)
        return PositionEpoch(self.time, x, y, z)


# %%
"""
Now we can load the data from the files.

We have to files containing polar epochs.
"""
from pathlib import Path

# Time values are given as offset seconds since 2018-03-13 15:10:00
start_date = datetime(2018, 3, 13, 15, 10, 0)


def load_polar_epochs(filename: str) -> list[PolarEpoch]:
    polar_epochs = []
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


tachy_measurements = load_polar_epochs(Path(__file__) / ".." / "obsTachy.txt")
laser_measurements = load_polar_epochs(Path(__file__) / ".." / "obsDrone.txt")

# %%
"""
Before working with the data, we need to sort it by time.

For this, we write a custom bubblesort function and compare its performance with
the built-in `Array.sort` function.

To measure the performance, we create a custom Timer class.
"""
from copy import deepcopy


def bubble_sort(arr: list) -> list:
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


class Timer:
    _name: str
    _start: datetime

    def __init__(self, name="Unnamed Timer") -> None:
        self._name = name

    def __enter__(self):
        self._start = datetime.now()

    def __exit__(self, *args):
        interval = datetime.now() - self._start
        print(f"[{self._name}] Time elapsed: {interval.total_seconds()} s")


# Copy the arrays before sorting, so we don't modify the original data
arr_copy = deepcopy(tachy_measurements)
with Timer("bubble_sort"):
    bubble_sort(arr_copy)

arr_copy = deepcopy(tachy_measurements)
with Timer("list.sort"):
    arr_copy.sort()

# The timer shows that the built-in sort function is much faster than our custom
# bubblesort function, so we use it to sort our observations.
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

import numpy as np

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


for p in ground_positions:
    # Determine the grid cell for the current position
    xi, yi = pos_to_grid_index(p)

    # Add the height to the grid point
    Z[yi, xi] += p.z
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
We can now visualize the data in a 3d plot.
"""

import matplotlib.pyplot as plt

# Create a 3d scene viewed from a favorable angle
fig = plt.figure(figsize=(10, 10), dpi=300)
ax = fig.add_subplot(
    projection="3d",
    elev=30,
    azim=170,
    # we have some issues with the contour plot overlapping the wireframe,
    # so we disable the zorder computation
    computed_zorder=False,
)
ax.set_xlabel("x [m]")
ax.set_ylabel("y [m]")
ax.set_zlabel("z [m]")
ax.grid(False)


# Draw a contour plot of the heightmap at the xy plane
ax.contourf(X, Y, Z, cmap="inferno", zdir="z", offset=0, alpha=0.8)

# # Draw a scatter plot of the ground positions
# ax.scatter(
#     [p.x for p in ground_positions],
#     [p.y for p in ground_positions],
#     [p.z for p in ground_positions],
#     color="black",
#     s=0.1,
#     alpha=0.1,
# )

# Draw a (ghostly) wireframe of the heightmap on top
ax.plot_wireframe(X, Y, Z, color="black", alpha=0.1)


def draw_tachymeter(drone_index=170):
    # Draw a small tachymeter from 5 points :)
    tachymeter_center = PositionEpoch(start_date, x=-51.28, y=-4.373, z=1.34)
    tachymeter_head = tachymeter_center + PositionEpoch(start_date, 0.0, 0.0, 0.5)
    tachymeter_leg1 = tachymeter_center + PositionEpoch(start_date, -1.0, 0.0, -1.5)
    tachymeter_leg2 = tachymeter_center + PositionEpoch(start_date, 0.0, 1.0, -1.5)
    tachymeter_leg3 = tachymeter_center + PositionEpoch(start_date, 0.7, -0.7, -1.5)
    # draw lines from the center to each of the 4 extremities
    for pos in [tachymeter_leg1, tachymeter_leg2, tachymeter_leg3, tachymeter_head]:
        ax.plot(
            [tachymeter_center.x, pos.x],
            [tachymeter_center.y, pos.y],
            [tachymeter_center.z, pos.z],
            color="black",
        )
    # draw a dotted line from the tachymeter to a drone position
    ax.plot(
        [drone_positions[drone_index].x, tachymeter_head.x],
        [drone_positions[drone_index].y, tachymeter_head.y],
        [drone_positions[drone_index].z, tachymeter_head.z],
        color="red",
        linewidth=1.0,
        dashes=[2, 4],
    )


def draw_drone(drone_index=170):
    p = drone_positions[drone_index]
    x, y, z = p.x, p.y, p.z

    # Draw a small sphere at the drone position
    ax.scatter(x, y, z, color="black", s=10)

    # Draw laser lines from the drone to the ground
    xi, yi = pos_to_grid_index(p)
    d = 20
    for dx in np.arange(-d, d, 1):
        for dy in np.arange(-d, d, 1):
            p = grid_index_to_pos(xi + dx, yi + dy)
            ax.plot(
                [x, p.x],
                [y, p.y],
                [z, p.z],
                color="#ff000005",
            )


def draw_flight_path():
    ax.plot(
        [p.x for p in drone_positions],
        [p.y for p in drone_positions],
        [p.z for p in drone_positions],
        color="gray",
        dashes=[10, 5],
        linewidth=1,
        alpha=0.5,
    )


draw_flight_path()
draw_tachymeter(240)
draw_drone(240)


# %%
