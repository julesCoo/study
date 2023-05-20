from enum import Enum

import matplotlib.artist as artist
import matplotlib.lines as lines
import matplotlib.pyplot as plt
import matplotlib.text as text
import numpy as np
from cartopy import crs as ccrs

from epoch import Epoch, interpolate_position


class SatelliteType(Enum):
    """
    There are two types of satellites in the dataset: GRACE and GPS.
    """

    GRACE = 1
    GPS = 2


class SatelliteRenderer:
    """
    Renders an individual satellite visualization onto the world map.
    This class is optimized for animations.
    """

    # Information about the satellite and its orbit
    name: str
    type: SatelliteType
    epochs: list[Epoch]

    # Indices into the epoch array.
    # The satellites "tail" is rendered as a line between these positions.
    # During animation, these indices are updated as the satellite moves.
    tail_index: int = 0
    head_index: int = 0

    # Plot elements that are updated during animation
    tail: lines.Line2D
    head: lines.Line2D
    line_of_sight: lines.Line2D
    label: text.Text

    def __init__(self, name: str, epochs: list[Epoch]):
        self.name = name
        self.type = SatelliteType.GRACE if "grace" in name else SatelliteType.GPS
        self.epochs = epochs

    def setup(self, ax: plt.Axes):
        """
        Prepare the satellite visualization for animation.
        This method should be called once before the animation starts.
        It creates the plot elements that are later updated during animation.
        """

        color = "red" if self.type == SatelliteType.GRACE else "yellow"
        lon, lat = self.epochs[0].lon, self.epochs[0].lat

        self.tail = ax.plot(
            [],
            [],
            color=color,
            transform=ccrs.Geodetic(),
        )[0]
        self.head = ax.plot(
            [lon],
            [lat],
            color=color,
            marker="o",
            markersize=2,
            transform=ccrs.PlateCarree(),
        )[0]
        self.line_of_sight = ax.plot(
            [],
            [],
            color="orange",
            linewidth=0.5,
            transform=ccrs.Geodetic(),
        )[0]
        self.label = ax.text(
            lon,
            lat,
            self.name,
            color=color,
            verticalalignment="center",
            horizontalalignment="left",
            transform=ccrs.PlateCarree(),
        )

        ax.plot(
            [epoch.lon for epoch in self.epochs],
            [epoch.lat for epoch in self.epochs],
            color=color,
            # linewidth=0.1,
            alpha=0.1,
            transform=ccrs.Geodetic(),
        )

    def draw_tail(self, time: float) -> list[artist.Artist]:
        """
        The main animation method. This is called once per frame.
        It moves the satellite to the correct position given `time`,
        and updates the plot elements accordingly.
        """
        head_time = time
        tail_time = time - 5 / 60  # 5 minutes ago

        lons, lats = self.get_lons_lats(time)
        if len(lons) == 0:
            return []

        lon, lat = lons[-1], lats[-1]

        # And update the tail and label position accordingly
        self.tail.set_data(lons, lats)
        self.head.set_data(lon, lat)
        self.label.set_position((lon, lat))

        return [self.tail, self.head, self.label]

    def draw_line_of_sight(self, grace: "SatelliteRenderer") -> list[artist.Artist]:
        """
        Draw a line between this (GPS) satellite and the GRACE satellite,
        if the GPS satellite can see the GRACE satellite.
        """

        if self.type == SatelliteType.GRACE:
            # doesn't apply, we don't draw lines from GRACE to GRACE
            return []

        # Figure out whether we are visible to grace.
        # For this, we consider the current xyz positions of both satellites.
        gps_epoch = self.epochs[self.head_index]
        gps_pos = np.array([gps_epoch.x, gps_epoch.y, gps_epoch.z])

        grace_epoch = grace.epochs[grace.head_index]
        grace_pos = np.array([grace_epoch.x, grace_epoch.y, grace_epoch.z])

        # Calculate two (unit) vectors, one going from GRACE to nadir
        # (which is already the origin of the coordinate system),
        # the other going from GRACE to the GPS satellite.
        e1 = grace_pos
        e1 /= np.linalg.norm(e1)
        e2 = grace_pos - gps_pos
        e2 /= np.linalg.norm(e2)

        # If the angle between these two vectors is greater than 90°,
        # that means that the GPS is "on top" of GRACE and can see it.
        alpha = np.arccos(np.dot(e1, e2))
        is_visible = alpha > np.pi / 2

        # Draw the line of sight if we can see GRACE,
        # otherwise don't draw anything.
        if is_visible:
            self.line_of_sight.set_data(
                [gps_epoch.lon, grace_epoch.lon],
                [gps_epoch.lat, grace_epoch.lat],
            )
        else:
            self.line_of_sight.set_data(
                [],
                [],
            )

        return [self.line_of_sight]

    def restart(self):
        """
        Reset the animation state to the beginning,
        so that the animation can be played again.
        """
        self.tail_index = 0
        self.head_index = 0

    def get_lons_lats(self, target_time):
        head_time = target_time

        lat, lon, dlat, dlon = interpolate_position(self.epochs, head_time)
        return (
            [lon - dlon * 5, lon],
            [lat - dlat * 5, lat],
        )
