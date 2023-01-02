import os
import PIL
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

PIL.Image.MAX_IMAGE_PIXELS = 933120000
os.chdir(os.path.dirname(__file__))

img = plt.imread("data/Klimazonen/CZ_4550.tif")[:, :, 0]
data = pd.read_csv("data/Klimazonen/CZ_4550.csv")

print(img.shape)

plt.imshow(img, cmap="jet", vmin=0, vmax=12)
plt.show()
