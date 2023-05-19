import datetime
from abc import ABC, abstractmethod
from typing import Optional

import matplotlib.animation as animation
import matplotlib.artist as artist
import matplotlib.pyplot as plt
import numpy as np
from cartopy import crs as ccrs
from loader import load_background_image, load_satellite_orbits
from print import print_progress
from satellite import SatelliteRenderer, SatelliteType


class TimeBasedAnimation(ABC):
    """
    Abstract base class for animations that visualize some real-time data.
    Can be used to control the playback speed and FPS of the animation.
    Implementers must implement the `setup`, `restart` and `update` methods.
    """

    num_frames: int
    time_range: tuple[float, float]

    time_per_second: float
    frames_per_second: int

    def __init__(
        self,
        time_range: tuple[float, float],
        time_per_second: float,
        frames_per_second: int = 30,
    ):
        self.time_range = time_range
        self.time_per_second = time_per_second
        self.frames_per_second = frames_per_second
        self.num_frames = int(
            (time_range[1] - time_range[0]) / time_per_second * frames_per_second
        )

    def start(self) -> animation.FuncAnimation:
        """
        Creates a new Figure object and starts the animation.
        """

        fig = plt.figure(figsize=(10, 10))

        # Subclass must setup the animation by adding artists to the figure.
        self.setup(fig)

        # This function is called for each frame of the animation.
        def next_frame(frame: int) -> list[artist.Artist]:
            print_progress("Rendering Animation Frames", frame + 1, self.num_frames)

            # Call `restart` on the first frame of each loop to allow subclasses
            # to reset their state.
            if frame == 0:
                self.restart()

            # Convert frame number into a time value to be used in the animation update.
            time = (
                self.time_range[0]
                + frame / self.frames_per_second * self.time_per_second
            )

            # Subclass must implement the `update` method to update the artists.
            return self.update(time)

        return animation.FuncAnimation(
            fig,
            next_frame,
            frames=self.num_frames,
            interval=1000 / self.frames_per_second,
            blit=True,
        )

    @abstractmethod
    def setup(fig: plt.Figure):
        """
        Subclasses must implement this method to create the artists used in the animation.
        """
        pass

    @abstractmethod
    def update(time: float) -> list[artist.Artist]:
        """
        Subclasses must implement this method to update the artists.
        The current real-world time is given as a parameter.
        """
        pass

    def restart():
        """
        Subclasses may implement this method to reset their state when the animation restarts.
        """
        pass


class OrbitsAnimation(TimeBasedAnimation):
    """
    This is the main animation class that visualizes the satellite orbits.
    """

    background_img: np.ndarray
    show_satellite_visibility: bool

    satellites: list[SatelliteRenderer]
    grace: Optional[SatelliteRenderer]

    def __init__(
        self,
        date: datetime.date,
        from_hour: float,
        to_hour: float,
        show_satellite_visibility: bool,
    ):
        super().__init__(
            time_range=(from_hour, to_hour),
            time_per_second=2,  # 2 hours per second, so 1 day takes 12 seconds
            frames_per_second=60,
        )

        # load the data used in this animation
        background_image = load_background_image(date)
        orbits = load_satellite_orbits(date)

        # setup renderers for each satellite
        satellites = []
        for name, epochs in orbits.items():
            satellite = SatelliteRenderer(name, epochs)
            satellites.append(satellite)

        # find the grace satellite in the list, if it exists
        grace = next(
            (
                satellite
                for satellite in satellites
                if satellite.type == SatelliteType.GRACE
            ),
            None,
        )

        self.show_satellite_visibility = show_satellite_visibility
        self.background_img = background_image
        self.satellites = satellites
        self.grace = grace

    def setup(self, fig: plt.Figure):
        """
        Setup the animation by creating the projection, adding the background image,
        then setup each satellite renderer.
        """

        ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax.set_global()
        ax.imshow(
            self.background_img,
            extent=[-180, 180, -90, 90],
            transform=ccrs.PlateCarree(),
        )

        for renderer in self.satellites:
            renderer.setup(ax)

    def update(self, time: float) -> list[artist.Artist]:
        """
        On each frame update, draw the updated positions of each satellite,
        then if `show_satellite_visibility` is enabled, draw the line of sight
        between the GPS satellites and the GRACE satellite.
        """

        updated_artists = []

        for renderer in self.satellites:
            updated_artists.extend(renderer.draw_tail(time))

        if self.show_satellite_visibility and self.grace:
            for renderer in self.satellites:
                updated_artists.extend(renderer.draw_line_of_sight(self.grace))

        return updated_artists

    def restart(self):
        for renderer in self.satellites:
            renderer.restart()
