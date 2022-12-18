from matplotlib import cm
from matplotlib import colors
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
import numpy as np
from pandas import DataFrame, read_csv
from os import path
from typing import Tuple
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.pyplot import subplots, imread
from scipy import interpolate
from matplotlib.path import Path

"""

Data Specifications

"""

# All ortho images used here show the exact same area,
# given in geodesic coordinates (x = north, y = east) as follows:
#
#     Image Size: 600 x 900 pixels
#       Top Left: x = 2100[m], y = -1100[m]
#   Bottom Right: x = 1500[m], y = -200[m]
#
# The coordinates found in the text files are given in cartesic coordinates (x = east, y = north).
# To avoid further confusion, we will from now on use only cartesic coordinates in this script.
width, height = 900, 600
x_min, x_max = -1100, -200
y_min, y_max = 1500, 2100

"""

Data Import 

"""

# All input files are located in the "data" subdirectory.
def data_file(name):
    return path.join(path.dirname(__file__), "data", name)


# All output files are located in the "results" subdirectory.
def result_file(name):
    return path.join(path.dirname(__file__), "results", name)


# Read image files via matplotlib API
def read_img(file: str) -> np.ndarray:
    return imread(data_file(file))


# Read surface data via pandas API
def read_surface_data(file: str) -> DataFrame:
    # some cleanup was required: remove trailing space, convert to utf8
    return read_csv(
        data_file(file),
        sep=" ",
        # First row is column headers
        header=0,
    )


# Read polylines via pandas API
def read_polyline(file: str) -> DataFrame:
    return read_csv(
        data_file(file),
        sep=",",
        # First row should be skipped according to specification.
        # It is unclear what data is contained there, but it certainly is not part of the polyline.
        skiprows=1,
        # These files don't contain a header, so we assign column names manually to match the names used in surface data.
        names=["X[m]", "Y[m]"],
    )


ortho_img_1953 = read_img("O1953_9960_A3_1m.tif")
ortho_img_1999 = read_img("O1999_9523_A3_1m.tif")
ortho_img_2004 = read_img("O2004_2385c_A3_1m.tif")

surface_1953 = read_surface_data("kr_53_A3_o25.dat")
surface_1999 = read_surface_data("kr_99_A3_o25.dat")

polyline_tear_edge = read_polyline("Anrisskante.bln")
polygon_tearoff_edge = read_polyline("Abbruchkante.bln")
polyline_region = read_polyline("diff_analyse_grd.bln")

"""

Surface Grid Interpolation

"""

# Data Points in the surface files are distributed irregularly over the region.
# To produce smooth surfaces for visualization, we need to interpolate the height values
# for each pixel in the ortho images.
# To do this, we first create a grid of the pixel coordinates.
grid_x, grid_y = np.meshgrid(
    np.linspace(x_min, x_max, width),
    np.linspace(y_min, y_max, height),
)

# We also create a list of all xy coordinate pairs, which is used later to create a mask for the region of interest.
grid_xy = np.vstack((grid_x.flatten(), grid_y.flatten())).T

# We can then interpolate the height values of each grid point using the surface data.
def interpolate_surface(surface: DataFrame) -> np.ndarray:
    return interpolate.griddata(
        points=(surface["X[m]"], surface["Y[m]"]),
        values=surface["Z[m]"],
        xi=(grid_x, grid_y),
        method="linear",
    )


grid_z_1953 = interpolate_surface(surface_1953)
grid_z_1999 = interpolate_surface(surface_1999)

# Calculate the height difference between the measurements in 1953 and 1999.
# This will be used for visualization later.
grid_z_diff = grid_z_1953 - grid_z_1999


"""

Surface Grid Visualization

"""

# We will visualize the surface data in two ways.

# First, we will plot contour lines in all the images.
# For this, the height values need to be clipped and binned into a reasonable range.
# Most of the height values are between 1500 and 2100 meters, so we will use this range and bin the values into 50 meter steps.
z_min, z_max, z_steps = 1500, 2100, 50

# Secondly, we will plot the height difference per pixel using a color map.
# Since we have difference values for every pixel of the ortho images (except some border pixels with undefined height),
# and we only want to show the data inside the region of interest, we need to create a mask for the data.

# This creates a closed path from the polyline data, which we can use to determine if a point is inside the region of interest.
# We then create a 2d array, which maps each pixel to a boolean value indicating if it is inside the region of interest.
region_path = Path(polyline_region[["X[m]", "Y[m]"]].values)
is_in_region = region_path.contains_points(grid_xy).reshape(grid_x.shape)

# And apply this as a mask to the height difference data.
# Since the mask function throws out values where the mask is true, we need to invert it first.
grid_z_diff = np.ma.masked_array(
    grid_z_diff,
    mask=np.logical_not(is_in_region),
)

# The height difference will be visualized via a custom color map.
# We want to show a range of -5 to 17 meters, and fade out the colorization between +- 0.5 meters,
# because no significant change happened in this area.
dz_min, dz_max, dz_steps = -5, 17, 1


def create_diff_colormap():
    # Use different base colormaps for positive and negative values
    top = cm.get_cmap("autumn_r")
    bottom = cm.get_cmap("summer")

    # Create a list of 256 colors, which will be used as the colormap
    colors = np.ndarray((256, 4))
    for i in range(256):
        # Height difference in meters at this index (interpolated in the dz range)
        dz = np.interp(i, [0, 255], [dz_min, dz_max])
        if dz > 0:
            # rescale dz to [0,255] as index in the "autumn_r" colormap.
            colors[i, :] = top(int(np.interp(dz, [0, dz_max], [0, 255])))
        else:
            # rescale dz to [0,255] as index in the "summer" colormap
            colors[i, :] = bottom(int(np.interp(dz, [dz_min, 0], [0, 255])))

        # Colors will be completely transparent for values between +- 0.5 meters.
        # Between +- 0.5 and 2 meters, we slowly fade in the color to avoid hard transitions.
        colors[i, -1] = np.interp(abs(dz), [0.5, 2], [0, 1])

    return ListedColormap(colors)


cmap_diff = create_diff_colormap()

"""

Base Map Generation

"""


def plot_basemap(title: str, ortho_image: np.ndarray, output_file: str):
    fig, ax = subplots()

    fig.suptitle("Hangrutschung im Blaubachgraben", fontsize=14, fontweight="bold")
    ax.set_title(title)
    ax.set_xlabel("east [m]")
    ax.set_ylabel("north [m]")
    ax.set_ylabel("north [m]")

    ax.imshow(ortho_image, extent=[x_min, x_max, y_min, y_max], cmap="gray")

    height_contours = ax.contour(
        grid_x,
        grid_y,
        grid_z_1999,
        levels=np.arange(z_min, z_max, z_steps),
        colors="black",
        linewidths=0.75,
    )
    ax.clabel(height_contours, inline=True, fontsize=10)

    # Tear Edge (dotted line)
    ax.plot(
        polyline_tear_edge["X[m]"],
        polyline_tear_edge["Y[m]"],
        color="red",
        linewidth=2,
        linestyle="--",
        label="Anrisskante",
    )

    # Tear-off Edge (solid line)
    ax.plot(
        polygon_tearoff_edge["X[m]"],
        polygon_tearoff_edge["Y[m]"],
        color="red",
        linewidth=2,
        label="Abbruchkante",
    )

    # Region outline (blue polygon)
    ax.plot(
        polyline_region["X[m]"],
        polyline_region["Y[m]"],
        color="blue",
        linewidth=2,
        label="Studienbereich",
    )

    ax.legend(loc="upper right")

    # Save to output file
    fig.savefig(result_file(output_file), dpi=400)

    return fig, ax


"""

Thematic Map Generation

"""


def plot_thematic_map(title: str, basemap: Tuple[Figure, Axes], output_file: str):
    fig, ax = basemap

    ax.set_title(title)

    diff_colors = ax.contourf(
        grid_x,
        grid_y,
        grid_z_diff,
        levels=np.arange(dz_min, dz_max, dz_steps),
        cmap=cmap_diff,
    )

    diff_colors_bar = fig.colorbar(diff_colors)
    diff_colors_bar.ax.set_title("$\Delta$H [m]")

    # Save to output file
    fig.savefig(result_file(output_file), dpi=400)

    return fig, ax


basemap_1953 = plot_basemap(
    title="Grundkarte 1953",
    ortho_image=ortho_img_1953,
    output_file="Grundkarte_1953.png",
)
# basemap_1999 = plot_basemap(
#     title="Grundkarte 1999",
#     ortho_image=ortho_img_1999,
#     output_file="Grundkarte_1999.png",
# )
# basemap_2004 = plot_basemap(
#     title="Grundkarte 2004",
#     ortho_image=ortho_img_2004,
#     output_file="Grundkarte_2004.png",
# )

plot_thematic_map(
    title="Differenz der Geländehöhen 1953 - 1999",
    basemap=basemap_1953,
    output_file="Differenz_1953_1999.png",
)
