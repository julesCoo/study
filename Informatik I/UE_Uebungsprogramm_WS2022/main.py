import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import interpolate


"""

Data Import 

"""


def data_file(name):
    return os.path.join(os.path.dirname(__file__), "data", name)


def result_file(name):
    return os.path.join(os.path.dirname(__file__), "results", name)


def read_surface_data(file: str) -> pd.DataFrame:
    # some cleanup was required: remove trailing space, convert to utf8
    return pd.read_csv(
        data_file(file),
        sep=" ",
        header=0,
    )


def read_polyline(file: str) -> pd.DataFrame:
    # Skip first row (no idea what's contained there, but it's not part of the polygon)
    return pd.read_csv(
        data_file(file),
        sep=",",
        skiprows=1,
        names=["X[m]", "Y[m]"],
    )


surface_1953 = read_surface_data("kr_53_A3_o25.dat")
surface_1999 = read_surface_data("kr_99_A3_o25.dat")

polyline_tear_edge = read_polyline("Anrisskante.bln")
polygon_tearoff_edge = read_polyline("Abbruchkante.bln")
polyline_region = read_polyline("diff_analyse_grd.bln")

"""

Base definitions

"""

# All orthophotos contain a rectangle of these coordinates.
# Careful: In the specification, geodesic coordinates were given (x = north, y = east),
# but in the data files, cartesic coordinates are used (x = east, y = north).
# We opt for cartesic coordinates, as they are the default in matplotlib.
x_min, x_max = -200, -1100
y_min, y_max = 1500, 2100

# Regular grid coordinates for interpolation of height values (600x900)
grid_size = 900, 600
x_grid, y_grid = np.meshgrid(
    np.linspace(x_min, x_max, grid_size[0]),
    np.linspace(y_min, y_max, grid_size[1]),
)

# TODO?
z_min = 1500
z_max = 2100
z_step = 50


def interpolate_surface(surface: pd.DataFrame) -> np.ndarray:
    return interpolate.griddata(
        points=(surface["X[m]"], surface["Y[m]"]),
        values=surface["Z[m]"],
        xi=(x_grid, y_grid),
        method="linear",
    )


z_grid = interpolate_surface(surface_1999)


def create_basemap(
    ortho_image_name: str,
    year: int,
    result_file_name: str,
):
    plt.suptitle("Hangrutschung im Blaubachgraben", fontsize=14, fontweight="bold")
    plt.title(f"Grundkarte: {year}")

    plt.xlim(x_max, x_min)
    plt.ylim(y_min, y_max)

    plt.imshow(
        plt.imread(data_file(ortho_image_name)),
        # x-axis flipped!
        extent=[x_max, x_min, y_min, y_max],
        cmap="gray",
    )

    height_contours = plt.contour(
        x_grid,
        y_grid,
        z_grid,
        levels=np.arange(z_min, z_max, z_step),
        colors="black",
        linewidths=0.75,
    )
    plt.clabel(height_contours, inline=True, fontsize=10)

    # Region outline (blue polygon)
    plt.plot(
        polyline_region["X[m]"],
        polyline_region["Y[m]"],
        color="blue",
        linewidth=2,
        label="Studienbereich",
    )

    # Tear Edge (dotted line)
    plt.plot(
        polyline_tear_edge["X[m]"],
        polyline_tear_edge["Y[m]"],
        color="red",
        linewidth=2,
        linestyle="--",
        label="Anrisskante",
    )

    # Tear-off Edge (solid line)
    plt.plot(
        polygon_tearoff_edge["X[m]"],
        polygon_tearoff_edge["Y[m]"],
        color="red",
        linewidth=2,
        label="Abbruchkante",
    )

    plt.xlabel("east [m]")
    plt.ylabel("north [m]")
    plt.legend(loc="upper right")

    plt.savefig(result_file(result_file_name), dpi=400)
    plt.close()


create_basemap(
    year=1953,
    ortho_image_name="O1953_9960_A3_1m.tif",
    result_file_name="img_1953.png",
)

create_basemap(
    year=1999,
    ortho_image_name="O1999_9523_A3_1m.tif",
    result_file_name="img_1999.png",
)

create_basemap(
    year=2004,
    ortho_image_name="O2004_2385c_A3_1m.tif",
    result_file_name="img_2004.png",
)
