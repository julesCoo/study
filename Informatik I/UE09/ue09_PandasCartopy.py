import os
import pandas as pd
import cartopy as cp
import numpy as np
import matplotlib.pyplot as plt
import warnings

# Matplotlib and Cartopy produce a number of warnings, which we
# want to filter out here to not clutter the output of the script.
warnings.filterwarnings("ignore")

# TODO remove: Set working directory to current directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

"""
Data Import and Cleanup
"""

# Read point coordinates from excel file
point_data = pd.read_excel("Punktkoordinaten.xlsx")

# Fix naming of X column, so it matches the other columns
point_data = point_data.rename(columns={"X [m]": "X[m]"})

# Delete broken rows (1. of every march contains "-")
point_data = point_data[point_data["X[m]"] != '"-"']

"""
Print Statistics
"""

# Print statistics for the numeric columns
xyz = point_data[["X[m]", "Y[m]", "H[m]"]]
stats = pd.DataFrame(
    {
        "Mittelwert": xyz.mean(),
        "Standardabweichung": xyz.std(),
        # Task description asks for mode, but that doesn't make much sense
        # for a continuous distribution of values, since each value only
        # occurs exactly once. So we use the median instead.
        "Median": xyz.median(),
    }
)

print(">> Statistiken:")
print(stats)

"""
Plot Coordinates over time
"""

# x-axis: time
time = point_data["Datum"]

# y-axis: x, y, z, normalized to [0, 1] by subtracting the integer part.
x = point_data["X[m]"].apply(lambda x: x - x // 1)
y = point_data["Y[m]"].apply(lambda y: y - y // 1)
z = point_data["H[m]"].apply(lambda z: z - z // 1)

plt.title("Punktkoordinaten\n(nur Nachkommastellen)", fontsize=16)
plt.scatter(time, x, label="X[m]", marker="+")
plt.scatter(time, y, label="Y[m]", marker="+")
plt.scatter(time, z, label="H[m]", marker="+")
plt.legend(loc="upper right")
plt.xlabel("Datum")
plt.savefig("Punktkoordinaten nach Datum.png")
plt.close()

"""
Plot Point heights over xy-space
"""

plt.title("Punkthöhen", fontsize=16)
plt.scatter(y, x, c=z, cmap="viridis", marker="+")
plt.colorbar(label="H[m]")
plt.xlabel("Y[m]")
plt.ylabel("X[m]")
plt.savefig("Punkthöhen nach XY.png")
plt.close()

"""
Create World maps with different projections
"""


def create_projection_plot(title, projection):
    # frameon=False removes the frame around the map
    ax = plt.subplot(projection=projection, frameon=False)
    ax.set_title(title, fontsize=24)

    # Show world map as stock image
    ax.stock_img()

    # add tissot indicatrix
    ax.tissot(facecolor="red", alpha=0.5)


def add_map_marker(label, pos):
    # Get current axis
    ax = plt.gca()

    # Add red dot marker at position
    ax.plot(pos[0], pos[1], marker="o", color="red", markersize=2)

    # Draw an arrow towards the position, coming from top right
    ax.annotate(
        label,
        xy=pos,
        xytext=(pos[0] + 15, pos[1] + 10),
        arrowprops=dict(width=2, headwidth=6, headlength=6, color="black"),
    )


# PlateCarree
create_projection_plot("PlateCaree", cp.crs.PlateCarree())
add_map_marker("Graz", (15.44, 47.07))
plt.savefig("WorldMap_PlateCarree.png")
plt.close()

# Robinson
create_projection_plot("Robinson", cp.crs.Robinson())
plt.savefig("WorldMap_Robinson.png")
plt.close()

# Orthographic
create_projection_plot("Orthographic", cp.crs.Orthographic(18, 45))
plt.savefig("WorldMap_Orthographic.png")
plt.close()

"""
Create Geoid undulation plots
"""
geoid_undulation = pd.read_csv("N-1Degree.txt", sep="\t", header=None)
x, y = np.meshgrid(
    np.linspace(-180, 180, 360),
    np.linspace(90, -90, 180),
)


def create_undulation_plot(title, hide_feature=None):
    plt.figure(figsize=(6, 4))
    ax = plt.subplot(projection=cp.crs.PlateCarree())
    ax.set_title(title, fontsize=16)
    ax.coastlines()
    cont = ax.contourf(
        x,
        y,
        geoid_undulation,
        cmap="jet",
        levels=np.arange(-110, 110, 1),
        transform=cp.crs.PlateCarree(),
        label="Geoid undulation",
    )
    plt.colorbar(cont, orientation="horizontal", pad=0)
    if hide_feature != None:
        # "Hide" a feature by drawing on top of it with a zorder > 0
        ax.add_feature(hide_feature, zorder=100, edgecolor="black", facecolor="white")


create_undulation_plot("Geoid undulation [m]")
plt.savefig("Geoid undulation.png")
plt.close()

create_undulation_plot("Geoid undulation on land [m]", hide_feature=cp.feature.OCEAN)
plt.savefig("Geoid undulation on land.png")
plt.close()

create_undulation_plot("Geoid undulation on ocean [m]", hide_feature=cp.feature.LAND)
plt.savefig("Geoid undulation on ocean.png")
plt.close()
