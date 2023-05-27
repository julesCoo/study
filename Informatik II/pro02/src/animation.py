import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from cartopy import crs as ccrs
from satellite import Satellite
from matplotlib.artist import Artist
from print import print_progress
import numpy as np


def create_keyframes(
    start_time: float,
    end_time: float,
    time_per_second: float = 1,
    frames_per_second: int = 30,
) -> list[float]:
    """
    Returns a list of keyframes for the animation.

    :param start_time: The start time of the animation.
    :param end_time: The end time of the animation.
    :param time_per_second: The time animated per second of animation.
    :param frames_per_second: The number of frames per second of animation.
    :return: A list of time values for the keyframes.
    """

    num_frames = int((end_time - start_time) / time_per_second * frames_per_second)
    return np.linspace(start_time, end_time, num_frames)


def create_animation(
    frames_per_second: int,
    keyframes: list[float],
    novisibility: bool,
    satellites: list[Satellite],
    background_image: np.ndarray,
) -> FuncAnimation:
    """
    Creates the animation.

    :param animation_data: The data for the animation.
    :param novisibility: Whether to hide the visibility of the satellites.
    :param background_image: The background image to use.
    :return: The animation.
    """

    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_global()
    ax.imshow(
        background_image,
        extent=[-180, 180, -90, 90],
        transform=ccrs.PlateCarree(),
    )

    for sat in satellites:
        sat.setup_animation(ax)

    grace = next(sat for sat in satellites if sat.is_grace)

    def update(frame: int) -> list[Artist]:
        """
        Updates the animation to the given time.

        :param time: The time to update the animation to.
        :return: The artists to draw.
        """

        print_progress("Rendering animation frames...", frame, len(keyframes))

        artists = []

        if not novisibility:
            for sat in satellites:
                artists += sat.update_visibility(frame, grace)

        for sat in satellites:
            artists += sat.update_position(frame)

        return artists

    return FuncAnimation(
        fig,
        update,
        frames=len(keyframes),
        interval=1000 / frames_per_second,
        blit=True,
    )
