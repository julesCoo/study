from typing import Tuple
import matplotlib.colors
import matplotlib.cm
import matplotlib.path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.interpolate
import io

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
# The coordinates found in the text files are given in mathematical coordinates (x = east, y = north).
# To avoid further confusion, we will from now on use only mathematical coordinates in this script.
width, height = 900, 600
x_min, x_max = -1100, -200
y_min, y_max = 1500, 2100

"""

Data Import 

"""

# Read image files via matplotlib API
def read_tif(filename: str) -> np.ndarray:
    return plt.imread(filename)


# Read surface data via pandas API
def read_dat(filename: str) -> pd.DataFrame:
    # .dat files are encoded in windows-1252 (boo!)
    with open(filename, "r", encoding="cp1252") as f:
        # They also contain a leading space in the header row, which confuses Pandas
        # (as it moves all columns to the right by one, which is incorrect!)
        # So we first have to remove that space and then pass the file contents to read_csv
        content = f.read()[1:]
        return pd.read_csv(io.StringIO(content), sep=" ", header=0)


# Read polylines via pandas API
def read_bln(filename: str) -> pd.DataFrame:
    return pd.read_csv(
        filename,
        sep=",",
        # First row should be skipped according to specification.
        # It is unclear what data is contained there, but it certainly is not part of the polyline.
        skiprows=1,
        # These files don't contain a header, so we assign column names manually to match the names used in surface data.
        names=["X[m]", "Y[m]"],
    )


ortho_img_1953 = read_tif("O1953_9960_A3_1m.tif")
ortho_img_1999 = read_tif("O1999_9523_A3_1m.tif")
ortho_img_2004 = read_tif("O2004_2385c_A3_1m.tif")

surface_1953 = read_dat("kr_53_A3_o25.dat")
surface_1999 = read_dat("kr_99_A3_o25.dat")
surface_2004 = read_dat("kr_9904_all.dat")

polyline_tear_edge = read_bln("Anrisskante.bln")
polyline_tearoff_edge = read_bln("Abbruchkante.bln")
polyline_region = read_bln("diff_analyse_grd.bln")

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
def interpolate_grid(
    surface: pd.DataFrame,
    x_column: str,
    y_column: str,
    z_column: str,
) -> np.ndarray:
    return scipy.interpolate.griddata(
        points=(surface[x_column], surface[y_column]),
        values=surface[z_column],
        xi=(grid_x, grid_y),
        method="linear",
    )


grid_z_1953 = interpolate_grid(surface_1953, "X[m]", "Y[m]", "Z[m]")
grid_z_1999 = interpolate_grid(surface_1999, "X[m]", "Y[m]", "Z[m]")
grid_z_2004 = interpolate_grid(surface_2004, "X1[m]", "Y1[m]", "Z1[m]")

# Calculate the height difference between the measurements in 1953 and 1999.
# This will be used for visualization later.
grid_z_diff_1999 = grid_z_1953 - grid_z_1999


# The difference between 1999 and 2004 can be read directly from the surface data
# of 2004.
grid_z_diff_2004 = interpolate_grid(surface_2004, "X1[m]", "Y1[m]", "dZ[m]")

grid_xy_diff_2004 = interpolate_grid(surface_2004, "X1[m]", "Y1[m]", "dS_2D/T[cm]")
grid_vec_u_2004 = interpolate_grid(surface_2004, "X1[m]", "Y1[m]", "dX/T[cm]")
grid_vec_v_2004 = interpolate_grid(surface_2004, "X1[m]", "Y1[m]", "dY/T[cm]")

"""

Surface Grid Visualization

"""

# We will visualize the surface data in two ways.

# First, we will plot contour lines in all the images.
# For this, the height values need to be clipped and binned into a reasonable range.
# Most of the height values are between 1500 and 2100 meters, so we will use this range and bin the values into 50 meter steps.
z_min, z_max, z_step = 1500, 2100, 50

# Secondly, we will plot the height difference per pixel using a color map.
# Since we have difference values for every pixel of the ortho images (except some border pixels with undefined height),
# and we only want to show the data inside the region of interest, we need to create a mask for the data.

# This creates a closed path from the polyline data, which we can use to determine if a point is inside the region of interest.
# We then create a 2d mask array, which maps each pixel to a boolean value indicating if it is outside the region of interest.
region_path = matplotlib.path.Path(polyline_region[["X[m]", "Y[m]"]].values)
region_mask = np.logical_not(region_path.contains_points(grid_xy).reshape(grid_x.shape))


# The height difference will be visualized via a custom color map.
# We want to show a range of -5 to 17 meters, and fade out the colorization between +- 0.5 meters,
# because no significant change happened in this area.
def create_diff_colormap(min, max):
    # Use different base colormaps for positive and negative values
    top = matplotlib.cm.get_cmap("autumn_r")
    bottom = matplotlib.cm.get_cmap("summer")

    # Create a list of 256 colors, which will be used as the colormap
    colors = np.ndarray((256, 4))
    for i in range(256):
        # Height difference in meters at this index (interpolated in the dz range)
        dz = np.interp(i, [0, 255], [min, max])
        if dz > 0:
            # rescale dz to [0,255] as index in the "autumn_r" colormap.
            colors[i, :] = top(int(np.interp(dz, [0, max], [0, 255])))
        else:
            # rescale dz to [0,255] as index in the "summer" colormap
            colors[i, :] = bottom(int(np.interp(dz, [min, 0], [0, 255])))

        # Colors will be completely transparent for values between +- 0.5 meters.
        # Between +- 0.5 and 2 meters, we slowly fade in the color to avoid hard transitions.
        colors[i, -1] = np.interp(abs(dz), [0.5, 2], [0, 1])

    cmap = matplotlib.colors.ListedColormap(colors)
    cmap.set_over(top(255))
    cmap.set_under(bottom(0))
    return cmap


"""

Base Map Generation

"""


def create_basemap(title: str, ortho_image: np.ndarray, grid_z: np.ndarray):
    fig, ax = plt.subplots()

    fig.suptitle("Hangrutschung im Blaubachgraben", fontsize=14, fontweight="bold")
    ax.set_title(title)

    ax.set_xlim(x_min, x_max)
    ax.set_xlabel("east [m]")

    ax.set_ylim(y_min, y_max)
    ax.set_ylabel("north [m]")

    ax.imshow(ortho_image, extent=[x_min, x_max, y_min, y_max], cmap="gray")

    height_contours = ax.contour(
        grid_x,
        grid_y,
        grid_z,
        levels=np.arange(z_min, z_max, z_step),
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
        polyline_tearoff_edge["X[m]"],
        polyline_tearoff_edge["Y[m]"],
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

    return fig


"""

Thematic Map Generation

"""


def create_colormap(
    title: str,
    ortho_image: np.ndarray,
    grid_z: np.ndarray,
    grid_values: np.ndarray,
    grid_levels: np.ndarray,
    cmap,
    ax_label="$\Delta$H [m]",
    extend="neither",
):
    fig = create_basemap(
        title=title,
        ortho_image=ortho_image,
        grid_z=grid_z,
    )
    ax = fig.axes[0]

    diff_colors = ax.contourf(
        grid_x,
        grid_y,
        np.ma.masked_array(grid_values, mask=region_mask),
        levels=grid_levels,
        cmap=cmap,
        extend=extend,
    )

    cax = fig.add_axes(
        [
            ax.get_position().x1 + 0.01,
            ax.get_position().y0,
            0.02,
            ax.get_position().height,
        ],
    )
    diff_colors_bar = fig.colorbar(diff_colors, cax=cax)
    diff_colors_bar.ax.set_title(ax_label)

    return fig


def create_vectormap(
    title: str,
    ortho_image: np.ndarray,
    grid_z: np.ndarray,
    grid_values: np.ndarray,
    grid_levels: np.ndarray,  # min, max, step
    grid_vec: Tuple[np.ndarray, np.ndarray],
    cmap,
    ax_label="H [m]",
):
    fig = create_colormap(
        title=title,
        ortho_image=ortho_image,
        grid_z=grid_z,
        grid_values=grid_values,
        grid_levels=grid_levels,
        cmap=cmap,
        ax_label=ax_label,
        extend="max",
    )
    ax = fig.axes[0]

    grid_vec_u, grid_vec_v = grid_vec
    grid_vec_u = np.ma.masked_array(grid_vec_u, mask=region_mask)
    grid_vec_v = np.ma.masked_array(grid_vec_v, mask=region_mask)

    # Specification calls for an arrow density of 1 arrow per 5 pixels, but this looks
    # way too crowded. Instead, we use 1 arrow per 25 pixels, which allows us to make
    # the arrows a bit thicker and easier to see.
    ax.quiver(
        grid_x[::25, ::25],
        grid_y[::25, ::25],
        grid_vec_u[::25, ::25],
        grid_vec_v[::25, ::25],
        units="xy",
        width=2,
        color="white",
        pivot="mid",
    )

    return fig


"""

Result File Generation

"""


create_basemap(
    title="Grundkarte 1953",
    ortho_image=ortho_img_1953,
    grid_z=grid_z_1953,
).savefig("Plot1_Grundkarte_1953.png", dpi=400)

create_basemap(
    title="Grundkarte 1999",
    ortho_image=ortho_img_1999,
    grid_z=grid_z_1999,
).savefig("Plot1_Grundkarte_1999.png", dpi=400)

create_basemap(
    title="Grundkarte 2004",
    ortho_image=ortho_img_2004,
    grid_z=grid_z_2004,
).savefig("Plot1_Grundkarte_2004.png", dpi=400)

create_colormap(
    title="Differenz der Geländeoberflächen\n1953 - 1999",
    ortho_image=ortho_img_1953,
    grid_z=grid_z_1999,
    grid_values=grid_z_diff_1999,
    grid_levels=np.arange(-5, 17, 1),
    cmap=create_diff_colormap(-5, 17),
).savefig("Plot2_Differenz_1953_1999.png", dpi=400)

create_colormap(
    title="Höhenänderung der Geländeoberflächen\n1999 - 2004",
    ortho_image=ortho_img_1999,
    grid_z=grid_z_2004,
    grid_values=grid_z_diff_2004,
    grid_levels=np.arange(-6, 6, 1),
    cmap=create_diff_colormap(-6, 6),
    extend="both",
).savefig("Plot2_Differenz_1999_2004.png", dpi=400)

create_vectormap(
    title="Mittlere jährliche Horizontalverschiebung\n1999 - 2004",
    ortho_image=ortho_img_1999,
    grid_z=grid_z_2004,
    grid_vec=(grid_vec_u_2004, grid_vec_v_2004),
    grid_values=grid_xy_diff_2004,
    grid_levels=np.arange(0, 180, 10),
    ax_label="$\Delta$xy [cm]",
    cmap="viridis",
).savefig("Plot3_Verschiebung_1999_2004.png", dpi=400)
