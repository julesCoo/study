import os
import PIL
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

PIL.Image.MAX_IMAGE_PIXELS = 933120000
os.chdir(os.path.dirname(__file__))

data = gpd.read_file("data/Flaechenwidmung.gpkg", rows=20000)
# data = data[data["Darstell"].isin([7, 19])]
# data.to_file("data/Flaechenwidmung_Forest.gpkg", driver="GPKG")

# data = gpd.read_file("data/Flaechenwidmung_Forest.gpkg")

# print all columns except "geometry"
# print(
#     data[
#         [
#             "WIDMUNG",
#             "ZSW",
#             # "MIND",
#             # "MAXD",
#             # "MAXH",
#             # "GEMNR",
#             # "ID_UPLOAD",
#             "Darstell",
#             "Beschrift",
#             "EBENE",
#             # "SCHNITTST",
#             # "gemnr_alt",
#             "INFOTXT",
#             # "GEMNR_NEU",
#             # "VFNR",
#         ]
#     ]
# )

# print all unique values of "WIDMUNG"
print(data["INFOTXT"].unique())

exit()

# split up rows accordint to the "Darstell" column
data_by_type = {}
for darstell in data["Darstell"].unique():
    data_by_type[darstell] = data[data["Darstell"] == darstell]

print(data_by_type.keys())

forest = data_by_type[7] + data_by_type[19]
print(forest.shape)

# plot polygons, filled with green
forest.plot(color="green")
# unknown.plot(color="black")
plt.show()

# img = plt.imread("data/Klimazonen/CZ_4550.tif")[:, :, 0]
# data = pd.read_csv("data/Klimazonen/CZ_4550.csv")

# print(img.shape)

# plt.imshow(img, cmap="jet", vmin=0, vmax=12)
# plt.show()
