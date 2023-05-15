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
    Abstract base class for animations that span some real-world time.
    Implementers must implement the `setup`, `restart` and `update` methods.
    """

    num_frames: int

    from_time: float
    to_time: float

    animation_speed: float
    frames_per_second: int

    def __init__(
        self,
        from_time: float,
        to_time: float,
        animation_speed: float,
        frames_per_second: int,
    ):
        self.from_time = from_time
        self.to_time = to_time
        self.animation_speed = animation_speed
        self.frames_per_second = frames_per_second
        self.num_frames = int(
            (to_time - from_time) / animation_speed * frames_per_second
        )

    def start(self) -> animation.FuncAnimation:
        fig = plt.figure(figsize=(10, 10))
        self.setup(fig)

        def anim_func(frame: int) -> list[artist.Artist]:
            print_progress("Rendering Animation Frames", frame + 1, self.num_frames)
            if frame == 0:
                self.restart()

            time = (
                self.from_time + frame / self.frames_per_second * self.animation_speed
            )
            return self.update(time)

        return animation.FuncAnimation(
            fig,
            anim_func,
            frames=self.num_frames,
            interval=1000 / self.frames_per_second,
            blit=True,
        )

    @abstractmethod
    def setup(fig: plt.Figure):
        pass

    @abstractmethod
    def restart():
        pass

    @abstractmethod
    def update(time: float) -> list[artist.Artist]:
        pass


class OrbitsAnimation(TimeBasedAnimation):
    background_img: np.ndarray
    show_satellite_visibility: bool

    all_satellites: list[SatelliteRenderer] = []
    gps_satellites: list[SatelliteRenderer] = []
    grace: Optional[SatelliteRenderer] = None

    def __init__(
        self,
        date: datetime.date,
        from_hour: float,
        to_hour: float,
        show_satellite_visibility: bool,
    ):
        super().__init__(
            from_time=from_hour,
            to_time=to_hour,
            animation_speed=4,
            frames_per_second=10,
        )

        self.show_satellite_visibility = show_satellite_visibility
        self.background_img = load_background_image(date)

        orbits = load_satellite_orbits(date)
        for name, epochs in orbits.items():
            sat = SatelliteRenderer(name, epochs)
            self.all_satellites.append(sat)
            if sat.type == SatelliteType.GPS:
                self.gps_satellites.append(sat)
            if sat.type == SatelliteType.GRACE:
                self.grace = sat

    def setup(self, fig: plt.Figure):
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax.set_global()

        # use the appropriate background image for this date
        # the image is a PlateCarree projected image of the earth,
        # which is reprojected to Robinson here
        ax.imshow(
            self.background_img,
            extent=[-180, 180, -90, 90],
            transform=ccrs.PlateCarree(),
        )

        for renderer in self.all_satellites:
            renderer.setup(ax)

    def restart(self):
        for renderer in self.all_satellites:
            renderer.restart()

    def update(self, time: float) -> list[artist.Artist]:
        artists = []
        for renderer in self.all_satellites:
            artists.extend(renderer.draw_tail(time))
        if self.show_satellite_visibility and self.grace:
            for renderer in self.gps_satellites:
                artists.extend(renderer.draw_line_of_sight(self.grace))
        return artists
