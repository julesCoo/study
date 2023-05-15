from dataclasses import dataclass

import numpy as np


@dataclass
class Epoch:
    """
    Represents a satellite position at a specific point in time.
    Position is given both in geocentric cartesian coordinates,
    as well as latitude and longitude.
    """

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
    """
    Load orbit data from the given file and apply some preprocessing
    to produce a list of Epochs.
    """

    # Data is given in tabular format, with the first two rows being headers.
    # First column is modified julian date, the other three are x, y, z coordinates.
    mjd, x, y, z = np.loadtxt(file_path, skiprows=2).T

    # Convert MJD to the abstract `time` value, which is
    # the number of hours since the start of the day in UT.
    # We throw away the date part, since this is already defined
    # by the file and is not relevant afterwards.
    time = (mjd - mjd.astype(int)) * 24

    # Convert cartesian coordinates to spherical coordinates.
    r = np.sqrt(x**2 + y**2 + z**2)
    phi = np.degrees(np.arcsin(z / r))
    theta = np.degrees(np.arctan2(y, x))

    # Create a list of Epochs from the data.
    epochs = []
    for i in range(len(mjd)):
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

    # Later processing requires Epochs to be sorted by time
    epochs = sorted(epochs, key=lambda epoch: epoch.time)

    return epochs
