# %%
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cartopy.crs as ccrs
from loader import load_satellites, load_background_image
from Satellite import SatelliteRenderer
import pandas as pd
import numpy as np


def generate_animation(
    date: datetime.date,
    from_time: datetime.time,
    to_time: datetime.time,
    visibility=True,
) -> plt.Figure:
    background_img = load_background_image(date)
    satellites = load_satellites(date)

    # setup Robinson projection plot (whole earth)
    # ax = plt.axes(projection=ccrs.Orthographic(central_latitude=80))
    ax = plt.axes(projection=ccrs.Robinson())
    ax.set_global()

    # use the appropriate background image for this date
    # the image is a PlateCarree projected image of the earth,
    # which is reprojected to Robinson here
    ax.imshow(
        background_img,
        extent=[-180, 180, -90, 90],
        transform=ccrs.PlateCarree(),
    )

    # create renderers for each satellite
    satellite_renderers = [SatelliteRenderer(ax, sat) for sat in satellites]
    grace_renderer = next(
        (r for r in satellite_renderers if r.satellite.is_grace()), None
    )

    last_time = 0

    def update(time):
        # restart the animation if we looped around
        nonlocal last_time
        if time < last_time:
            for renderer in satellite_renderers:
                renderer.restart()
        last_time = time

        # on each frame, update all the renderers
        artists = []
        for renderer in satellite_renderers:
            artists.extend(renderer.update(time))

        if grace_renderer:
            for renderer in satellite_renderers:
                artists.extend(renderer.draw_connector(grace_renderer))

        return artists

    anim = animation.FuncAnimation(
        fig=ax.figure,
        func=update,
        frames=np.arange(0, 24, 0.05),
        interval=20,
        blit=True,
    )

    # measure_update_perf(anim)


def measure_update_perf(anim: animation.FuncAnimation):
    # Set the number of update iterations to measure
    num_iterations = 10

    # Start the timer
    start_time = time.time()

    # Perform the update iterations
    for i in range(num_iterations):
        print("simulating iteration " + str(i))
        anim._step()

    # Stop the timer
    end_time = time.time()

    # Calculate the average duration per update
    duration_per_update = (end_time - start_time) / num_iterations * 1000
    print(f"Duration per update: {duration_per_update:.2f} ms")
