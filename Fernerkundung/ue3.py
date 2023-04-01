# %%
"""
Prepare for loading Landsat images
"""
import rasterio
from rasterio.io import DatasetReader
from pathlib import Path
from datetime import datetime


def open_landsat_file(
    level: int = 2,
    start_path: int = 190,
    start_row: int = 27,
    end_row: int = 27,
    aq_date: datetime = datetime(2007, 9, 14),
    file_type: str = "B80",
) -> DatasetReader:
    filename = "".join(
        [
            "L7",
            f"{level:01d}",
            f"{start_path:03d}",
            f"{start_row:03d}",
            "_",
            f"{end_row:03d}",
            f"{aq_date.strftime('%Y%m%d')}",
            "_",
            file_type,
            ".TIF",
        ]
    )
    path = Path(__file__) / ".." / "data1" / "LS7" / "LS2007" / filename
    return rasterio.open(path)


# %%
"""
Load a panchromatic image and show its metadata
"""

band_8_pan = open_landsat_file(level=2, file_type="B80")
band_8_pan.meta

# %%
"""
Read its image data and plot a subset
"""

import matplotlib.pyplot as plt

plt.imshow(
    band_8_pan.read(1, window=((9800, 11500), (6500, 8000))),
    cmap="gray",
)

# %%
"""
Layer stacking: Combine multiple bands into a single .img file
"""

band_1_bg = open_landsat_file(level=1, file_type="B10")
band_2_g = open_landsat_file(level=1, file_type="B20")
band_3_r = open_landsat_file(level=1, file_type="B30")
band_4_nir = open_landsat_file(level=1, file_type="B40")
band_5_mir1 = open_landsat_file(level=1, file_type="B50")
band_6_mir2 = open_landsat_file(level=2, file_type="B70")

meta = band_8_pan.meta.copy()
meta["count"] = 6

# This will take a while
with rasterio.open("results/ls2007_ms_notir.img", "w", **meta) as dest:
    dest.write(band_1_bg.read(1), 1)
    dest.write(band_2_g.read(1), 2)
    dest.write(band_3_r.read(1), 3)
    dest.write(band_4_nir.read(1), 4)
    dest.write(band_5_mir1.read(1), 5)
    dest.write(band_6_mir2.read(1), 6)

# %%
"""
Create a subset
"""

# Coordinates for group 2
x0, y0 = 511920, 5326920
x1, y1 = x0 + 18000, y0 + 18000

# %%
"""
Plot the subset as panchromatic image
"""

# convert coordinates to pixel indices from the panchromatic image (x-axis is flipped!)
row0, col0 = band_8_pan.index(x0, y0)
row1, col1 = band_8_pan.index(x1, y1)
window = ((col0, col1), (row1, row0))
plt.imshow(band_8_pan.read(1, window=window), cmap="gray")

# %%
"""
Plot the subset as multispectral image
"""
import numpy as np

# convert coordinates to pixel indices from the multispectral image (x-axis is flipped!)
row0, col0 = band_1_bg.index(x0, y0)
row1, col1 = band_1_bg.index(x1, y1)
window = ((col0, col1), (row1, row0))

# create an rgb image from BG, G and R bands
rgb = np.dstack(
    [
        band_1_bg.read(1, window=window),
        band_2_g.read(1, window=window),
        band_3_r.read(1, window=window),
    ]
)

plt.imshow(rgb)


# %%
