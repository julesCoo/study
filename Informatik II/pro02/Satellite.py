from dataclasses import dataclass
from cartopy import crs as ccrs
from typing import Any
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.artist as artist


@dataclass
class Epoch:
    # a float representing the time in hours since the start of the day
    time: float

    # the latitude and longitude of the satellite at this time
    lat: float
    lon: float


@dataclass
class Satellite:
    name: str
    epochs: list[Epoch]
    df: pd.DataFrame

    @staticmethod
    def load_from_file(file_path: str) -> "Satellite":
        # file path ends with YYYY-MM-DD.sat.gz.txt
        # so we can extract the name of the satellite from it.
        name = file_path.split(".")[-3]

        # load the orbit data from the file. first two lines are headers
        mjd, x, y, z = np.loadtxt(file_path, skiprows=2).T
        num_rows = len(mjd)

        # preprocessing: derive latitude, longitude and time from the orbit data
        time = (mjd - mjd.astype(int)) * 24
        r = np.sqrt(x**2 + y**2 + z**2)
        phi = np.degrees(np.arcsin(z / r))
        theta = np.degrees(np.arctan2(y, x))

        df = pd.DataFrame(
            {
                "time": time,
                "lat": phi,
                "lon": theta,
                "x": x,
                "y": y,
                "z": z,
            }
        )
        df.sort_values(by="time", inplace=True)

        # convert to epochs
        epochs = []
        for i in range(num_rows):
            epochs.append(
                Epoch(
                    time=time[i],
                    lat=phi[i],
                    lon=theta[i],
                )
            )

        # sort epochs by time, to speed up later lookups
        epochs = sorted(epochs, key=lambda epoch: epoch.time)

        return Satellite(name, epochs, df)


class SatelliteRenderer:
    # the satellite to render
    satellite: Satellite

    # indices into the epoch array of the satellite
    # we render the segment between these indices to draw the "tail"
    # of the satellite
    lower_bound: int
    upper_bound: int

    # the artists that are updated during the animation
    line: plt.Line2D
    text: plt.Text

    def __init__(
        self,
        ax: plt.Axes,
        satellite: Satellite,
    ):
        self.satellite = satellite
        self.lower_bound = 0
        self.upper_bound = 0

        color = "red" if "grace" in satellite.name else "yellow"

        # prepare the animation by rendering the initial state
        # into the axes. later we will only update the artists
        # that are created here
        lon, lat = satellite.df.at[0, "lon"], satellite.df.at[0, "lat"]

        self.line = ax.plot(
            lon,
            lat,
            color=color,
            transform=ccrs.Geodetic(),
        )[0]

        self.text = ax.text(
            lon,
            lat,
            satellite.name,
            color=color,
            verticalalignment="center",
            horizontalalignment="left",
            transform=ccrs.Geodetic(),
        )

    def update(self, time: float) -> list[artist.Artist]:
        df = self.satellite.df
        count = len(df)

        lower_bound_time = time - 1 / 4  # 15 minutes before now
        upper_bound_time = time

        # seek the lower_bound to the first index that is after the given time - dT
        while (
            self.lower_bound < count
            and df.at[self.lower_bound, "time"] < lower_bound_time
        ):
            self.lower_bound += 1

        # seek the upper_bound to the first index that is after the given time
        while (
            self.upper_bound < count
            and df.at[self.upper_bound, "time"] < upper_bound_time
        ):
            self.upper_bound += 1

        # extract the lon and lat of the satellite at the given time
        lons = [row["lon"] for i, row in df.iloc[self.lower_bound:self.upper_bound + 1].iterrows()]
        lats = [row["lat"] for i, row in df.iloc[self.lower_bound:self.upper_bound + 1].iterrows()]


        self.line.set_data(lons, lats)
        self.text.set_position((lons[-1], lats[-1]))

        return [self.line, self.text]
