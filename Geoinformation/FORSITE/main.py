import os
import PIL
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import pathlib
from scipy.ndimage import zoom
import rasterio
from rasterio.io import MemoryFile
from rasterio.transform import from_bounds
from rasterio.warp import calculate_default_transform
import shapely.geometry
from rasterio.features import geometry_mask

PIL.Image.MAX_IMAGE_PIXELS = 933120000

# Coordinates of Styria region
x0, y0 = 13.55, 47.82
x1, y1 = 16.18, 46.60

# Where to find the data
data_dir = pathlib.Path(__file__).parent.absolute() / "data"
fp_csv = data_dir / "Waldstandorte" / "hwg_hist.csv"
fp_tif = data_dir / "Waldstandorte" / "hwg_hist.tif"

# Image uses WGS84 transform
# Select the region of interest
left = 14
right = 15
top = 47
bottom = 46

# open the image but only load region of interest
with rasterio.open(fp_tif) as dataset:
    print(dataset.transform * (0, 0))
    print(dataset.crs)
    print(dataset.indexes)
    band1 = dataset.read(1, window=((5000, 6000), (5000, 6000)))
    print(band1.shape)
    plt.imshow(band1)
    plt.show()
