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
    ax = plt.axes(projection=ccrs.Robinson())
    ax.set_global()

    # use the appropriate background image for this date
    # the image is a PlateCarree projected image of the earth,
    # which is reprojected to Robinson here
    ax.imshow(background_img, transform=ccrs.PlateCarree())

    # create renderers for each satellite
    satellite_renderers = [SatelliteRenderer(ax, sat) for sat in satellites]

    def update(hour):
        # on each frame, update all the renderers
        artists = []
        for renderer in satellite_renderers:
            satellite_artists = renderer.update(hour)
            artists.extend(satellite_artists)
        return artists

    anim = animation.FuncAnimation(
        fig=ax.figure,
        func=update,
        frames=np.arange(0, 24, 0.05),
        interval=20,
        blit=True,
    )

    measure_update_perf(anim)
    # plt.show()


# %%


def measure_update_perf(anim: animation.FuncAnimation):
    # Set the number of update iterations to measure
    num_iterations = 100

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
