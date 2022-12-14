import matplotlib.pyplot as plt
from math import tau
import numpy as np

data = np.loadtxt("10.2 Q-Faktor.txt")

xs = data[:, 0]
ys = data[:, 1]

# find the local maxima
is_max = np.r_[True, ys[1:] > ys[:-1]] & np.r_[ys[:-1] > ys[1:], True]
is_max[-1] = False

# get the median distance between the maxima
wavelength = np.median(np.diff(xs[is_max]))

# convert to frequency
frequency = 2 * np.pi / wavelength

# get xy coordinates of the maxima
xs_max = xs[is_max]
ys_max = ys[is_max]

# get the exponential decay factor
decay = (xs_max[-1] - xs_max[0]) / np.log(ys_max[0] / ys_max[-1])

# get quality factor
q = frequency * decay / 2

print(frequency)
print(decay)
print(q)
