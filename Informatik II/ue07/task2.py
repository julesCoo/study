import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cartopy.crs as ccrs


def animate_graviational_field():
    # load the gravity field data from the gravityField.npy file
    # is a 3d matrix with dimensions [month] x [lat] x [lon]
    m = np.load("gravityField.npy")

    # data is given in meters but should be plotted in centimeters
    m *= 100

    # extract the dimensions of the data
    num_months = m.shape[0]
    lats = np.linspace(90, -90, m.shape[1])
    lons = np.linspace(-180, 180, m.shape[2])

    # setup a Robinson projection plot (global extend) with coastlines
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
    ax.set_title("Seasonal gravity signal from GRACE")
    ax.set_global()
    coast = ax.coastlines()

    # add a text denoting the current month somewhere in the ocean,
    # where it doesn't hide relevant details
    text_lon, text_lat = -130, 0
    text = ax.text(
        text_lon,
        text_lat,
        "Month: 2008-01",
        horizontalalignment="center",
        verticalalignment="bottom",
        transform=ccrs.PlateCarree(),
        fontsize=8,
        color="black",
    )

    # draw the gravity field of the first month into the plot as a color mesh
    grid = plt.pcolormesh(
        lons,
        lats,
        m[0, :, :],
        transform=ccrs.PlateCarree(),
        cmap="RdBu",
        vmin=-15,
        vmax=15,
    )

    # use a colorbar as a legend for the gravitational field
    plt.colorbar(
        grid,
        ax=ax,
        orientation="horizontal",
        aspect=50,
        pad=0.05,
        label="Equivalent water height [cm]",
        extend="both",
    )

    # on every animation frame, update the visualization (color mesh and text)
    # with data for the next month.
    # then repaint grid, text and coastlines
    def update_frame(i: int):
        grid.set_array(m[i, :, :].flatten())
        text.set_text(f"Month: 2008-{i+1:02d}")
        return [grid, text, coast]

    # let the animation loop over the 12 month, with a frame rate of 5 fps
    anim = animation.FuncAnimation(
        fig,
        update_frame,
        frames=num_months,
        interval=200,
        repeat=True,
        blit=True,
    )

    plt.show()
