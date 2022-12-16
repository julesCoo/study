import os
from PIL import Image, ImageDraw
import numpy as np
import pathlib

DATA_DIR = pathlib.Path(__file__).parent / "data_student"
OUT_DIR = pathlib.Path(__file__).parent

img = Image.open(f"{DATA_DIR}/O1953_9960_A3_1m.tif").convert("RGB")
draw = ImageDraw.Draw(img)

data = np.loadtxt(f"{DATA_DIR}/diff_analyse_grd.bln", delimiter=",")
# first line contains garbage values
data = data[1:]

# rescale to image coordinates
xs = np.interp(data[:, 0], [-1100, -200], [0, img.width])
ys = np.interp(data[:, 1], [1500, 2100], [0, img.height])

# draw polygon and save
points = list(zip(xs, ys))
draw.polygon(points, outline="red", width=2)

img.save(f"{OUT_DIR}/out.png")
