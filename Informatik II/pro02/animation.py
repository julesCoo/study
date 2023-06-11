# -*- coding: utf-8 -*-
"""
File: animation.py
Author: Daniel Ebert
Date: 06.06.2023

Description:
    This file manages the animation at a high level, without going into 
    details about how the satellite orbits are rendered.
"""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from cartopy import crs as ccrs
from satellite import Satellite
from labels import FrameLabel, TimeLabel, Legend
from matplotlib.artist import Artist
from print import print_progress
import numpy as np
from datetime import datetime, timedelta


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
    date: datetime,
    keyframes: list[float],
    show_visibility: bool,
    satellites: list[Satellite],
    background_image: np.ndarray,
) -> FuncAnimation:
    """
    Creates the animation.

    :param animation_data: The data for the animation.
    :param show_visibility: Whether to hide the visibility of the satellites.
    :param background_image: The background image to use.
    :return: The animation.
    """

    # Find the grace satellite.
    grace = next((sat for sat in satellites if sat.is_grace), None)
    if grace is None:
        raise Exception("No GRACE satellite found for this date.")

    # Setup the projection plot with the background image.
    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_global()
    ax.imshow(
        background_image,
        extent=[-180, 180, -90, 90],
        transform=ccrs.PlateCarree(),
    )

    # Add dynamic plot elements
    time_label = TimeLabel(date, keyframes)
    time_label.setup_animation(ax)

    frame_label = FrameLabel(keyframes)
    frame_label.setup_animation(ax)

    for sat in satellites:
        sat.setup_animation(ax)

    Legend().setup_animation(ax)

    def update(frame: int) -> list[Artist]:
        """
        Updates the animation to the given time.

        :param time: The time to update the animation to.
        :return: The artists to draw.
        """

        updated_artists = []
        if frame > 0:
            print_progress("Rendering animation frames...", frame, len(keyframes))

        updated_artists += time_label.update(frame)
        updated_artists += frame_label.update(frame)

        if show_visibility:
            for sat in satellites:
                updated_artists += sat.update_visibility(frame, grace)

        for sat in satellites:
            updated_artists += sat.update_position(frame)

        return updated_artists

    return FuncAnimation(
        fig,
        update,
        frames=len(keyframes),
        interval=1000 / frames_per_second,
        blit=True,
    )