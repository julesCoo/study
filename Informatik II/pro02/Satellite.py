from dataclasses import dataclass
from cartopy import crs as ccrs
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

    # geocentric coordinates of the satellite at this time
    x: float
    y: float
    z: float


@dataclass
class Satellite:
    name: str
    epochs: list[Epoch]

    def is_grace(self) -> bool:
        return "grace" in self.name

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

        # sort epochs by time, to speed up later lookups
        epochs = sorted(epochs, key=lambda epoch: epoch.time)

        return Satellite(name, epochs)


class SatelliteRenderer:
    # the satellite to render
    satellite: Satellite

    # indices into the epoch array of the satellite
    # we render the segment between these indices to draw the "tail"
    # of the satellite
    lower_bound: int
    upper_bound: int

    # the artists that are updated during the animation
    artist_tail: plt.Line2D
    artist_connector: plt.Line2D
    artist_label: plt.Text

    def __init__(
        self,
        ax: plt.Axes,
        satellite: Satellite,
    ):
        self.satellite = satellite
        self.lower_bound = 0
        self.upper_bound = 0

        color = "red" if satellite.is_grace() else "yellow"

        # prepare the animation by rendering the initial state
        # into the axes. later we will only update the artists
        # that are created here
        lon, lat = satellite.epochs[0].lon, satellite.epochs[0].lat

        self.artist_tail = ax.plot(
            [],
            [],
            color=color,
            transform=ccrs.Geodetic(),
        )[0]

        self.artist_connector = ax.plot(
            [],
            [],
            color="orange",
            linewidth=0.5,
            transform=ccrs.Geodetic(),
        )[0]

        self.artist_label = ax.text(
            lon,
            lat,
            satellite.name,
            color=color,
            verticalalignment="center",
            horizontalalignment="left",
            transform=ccrs.PlateCarree(),
        )

    def update(self, time: float) -> list[artist.Artist]:
        epochs = self.satellite.epochs
        count = len(epochs)

        lb = self.lower_bound
        lb_time = time - 1 / 4  # 15 minutes before now
        lb_epoch = epochs[lb]
        while lb_epoch.time < lb_time and lb < count - 1:
            lb += 1
            lb_epoch = epochs[lb]

        ub = self.upper_bound
        ub_time = time
        up_epoch = epochs[ub]
        while up_epoch.time < ub_time and ub < count - 1:
            ub += 1
            up_epoch = epochs[ub]

        # extract the lon and lat of the satellite at the given time
        lons = [epoch.lon for epoch in epochs[lb : ub + 1]]
        lats = [epoch.lat for epoch in epochs[lb : ub + 1]]

        self.artist_label.set_position((lons[-1], lats[-1]))
        self.artist_tail.set_data(lons, lats)

        self.lower_bound = lb
        self.upper_bound = ub
        return [self.artist_tail, self.artist_label]

    def draw_connector(
        self, grace_renderer: "SatelliteRenderer"
    ) -> list[artist.Artist]:
        my_epoch = self.satellite.epochs[self.upper_bound]
        grace_epoch = grace_renderer.satellite.epochs[grace_renderer.upper_bound]

        my_pos = np.array([my_epoch.x, my_epoch.y, my_epoch.z])
        grace_pos = np.array([grace_epoch.x, grace_epoch.y, grace_epoch.z])

        connection = grace_pos - my_pos
        alpha = np.arccos(
            np.dot(grace_pos, connection)
            / (np.linalg.norm(grace_pos) * np.linalg.norm(connection))
        )
        is_visible = alpha > np.pi / 2

        if is_visible:
            self.artist_connector.set_data(
                [my_epoch.lon, grace_epoch.lon],
                [my_epoch.lat, grace_epoch.lat],
            )
        else:
            self.artist_connector.set_data([], [])

        return [self.artist_connector]

    def restart(self):
        self.lower_bound = 0
        self.upper_bound = 0
