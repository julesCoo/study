# %%
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cartopy.crs as ccrs
from loader import load_satellites, load_background_image
from Satellite import SatelliteRenderer


def generate_animation(
    date: datetime.date,
    from_time: datetime.time,
    to_time: datetime.time,
    visibility=True,
) -> animation.FuncAnimation:
    print("Loading data...")
    background_img = load_background_image(date)
    satellites = load_satellites(date)

    print("Creating animation...")
    # setup Robinson projection plot (whole earth)
    # ax = plt.axes(projection=ccrs.Orthographic(central_latitude=80))
    ax = plt.axes(projection=ccrs.PlateCarree())
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

    animation_speed = 2  # hours of data per second of animation
    animation_frequency = 30  # frames per second

    real_time_total = to_time.hour - from_time.hour
    animation_time_total = real_time_total / animation_speed
    num_frames = int(animation_time_total * animation_frequency)

    def update(frame_num):
        print(f"rendering frame {frame_num+1} of {num_frames}")

        # restart the animation if we looped around
        if frame_num == 0:
            for renderer in satellite_renderers:
                renderer.restart()

        time = from_time.hour + frame_num / animation_frequency * animation_speed

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
        frames=num_frames,
        interval=1000 / animation_frequency,
        blit=True,
    )

    # measure_update_perf(anim)
    return anim


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
