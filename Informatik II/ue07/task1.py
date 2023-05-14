import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


def plot_grace_orbits():
    # load orbit data of one day from the orbit.txt file
    # is a matrix with columns [mjd], [x], [y], [z]
    mjd, x, y, z = np.loadtxt("orbit.txt", skiprows=2).T

    # convert cartesian coordinates to spherical coordinates
    r = np.sqrt(x**2 + y**2 + z**2)
    phi = np.arcsin(z / r)
    lamda = np.arctan2(y, x)

    # setup a plot using Robionson projection, whole earth
    ax = plt.axes(projection=ccrs.Robinson())
    ax.set_global()

    # use the bluemarble image as background.
    # the image is given in PlateCarree projection and will be
    # reprojected to the Robinson projection
    ax.imshow(
        plt.imread("bluemarble01.jpg"),
        extent=[-180, 180, -90, 90],
        transform=ccrs.PlateCarree(),
    )

    # plot the orbit of the satellite using a red line.
    # to connect the individual positions as lines on the sphere,
    # we need to use the Geodetic projection
    ax.plot(
        lamda * 180 / np.pi,
        phi * 180 / np.pi,
        color="red",
        linewidth=0.5,
        transform=ccrs.Geodetic(),
    )

    plt.show()
