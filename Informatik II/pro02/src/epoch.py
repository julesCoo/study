from dataclasses import dataclass

import numpy as np


@dataclass
class Epoch:
    # a float representing the time in hours since the start of the day
    time: float

    # the latitude and longitude of the satellite at this time
    lat: float
    lon: float

    # geocentric coordinates of the satellite at this time
    x: float
    y: float
    z: float


def load_epochs(file_path: str) -> list[Epoch]:
    # load the orbit data from the file. first two lines are headers
    mjd, x, y, z = np.loadtxt(file_path, skiprows=2).T
    num_rows = len(mjd)

    # preprocessing: derive latitude, longitude and time from the orbit data
    time = (mjd - mjd.astype(int)) * 24
    r = np.sqrt(x**2 + y**2 + z**2)
    phi = np.degrees(np.arcsin(z / r))
    theta = np.degrees(np.arctan2(y, x))

    # convert to epochs, for more performant lookups later
    epochs = []
    for i in range(num_rows):
        epochs.append(
            Epoch(
                time=time[i],
                lat=phi[i],
                lon=theta[i],
                x=x[i],
                y=y[i],
                z=z[i],
            )
        )

    # later processing requires Epochs to be sorted by time
    epochs = sorted(epochs, key=lambda epoch: epoch.time)
    return epochs
