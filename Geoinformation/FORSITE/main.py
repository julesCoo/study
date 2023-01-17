#%%
import numpy as np
import pathlib
import rasterio
import rasterio.windows
import rasterio.features
import matplotlib.pyplot as plt
import pyproj

# Where to find the data
data_dir = pathlib.Path(__file__).parent.absolute() / "data"
# fp_csv = data_dir / "Topographie" / "Dgm.csv"
fp_tif = data_dir / "Topographie" / "dgm.tif"
# fp_tif = data_dir / "Klimazonen" / "CZ_hist.tif"
# fp_tif = data_dir / "Waldgruppen" / "hwg_4550.tif"
fp_tif = data_dir / "Hauptwaldstandorte" / "hwsto_hist.tif"

dataset = rasterio.open(fp_tif)

# lat, lon = 47.18180603462566, 14.717421581467315
lat, lon = 47.17178876044296, 15.766503713838189
lat, lon = 47.41732089761018, 15.329019534710724

transformer = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:32633", always_xy=True)
x, y = transformer.transform(lon, lat)

window_size = 1000
window = rasterio.windows.from_bounds(
    left=x - window_size // 2,
    bottom=y - window_size // 2,
    right=x + window_size // 2,
    top=y + window_size // 2,
    transform=dataset.transform,
)


band1 = dataset.read(1, window=window)
# create a colormap from unique values

min = np.min(band1)
max = np.max(band1)
print(np.unique(band1))
plt.imshow(band1, vmin=min, vmax=max, cmap="tab20")

# extract polygons from raster
polys = list(rasterio.features.shapes(band1, transform=dataset.transform))
print(list(map(lambda x: x[1], polys)))

# %%
