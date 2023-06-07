# -*- coding: utf-8 -*-
"""
File: satellite.py
Author: Daniel Ebert
Date: 06.06.2023

Description: 
    This file deals with loading, preprocessing and rendering
    data of a single satellite.
"""

from dataclasses import dataclass
import matplotlib.pyplot as plt
from matplotlib.artist import Artist
from cartopy import crs as ccrs
import pandas as pd
import numpy as np


class Satellite:
    name: str
    df: pd.DataFrame

    def __init__(self, name: str, df: pd.DataFrame):
        self.name = name
        self.df = df

    @property
    def is_grace(self) -> bool:
        return self.name == "graceA"

    @staticmethod
    def load_from_file(filepath: str, keyframes: list[float]):
        """
        Loads Orbit data from a file and interpolates it to the given keyframes.
        Raw data from the file is preprocessed to calculate the latitude and longitude,
        as well as the change in latitude and longitude between two keyframes.
        """

        # File path ends with YYYY-MM-DD.SATNAME.gz.txt
        name = filepath.split(".")[-3]

        mjd, x, y, z = np.loadtxt(filepath, skiprows=2).T

        # Time values are given in MJD, while the keyframes use hours.
        # To interpolate, we need to convert the MJD values to hours
        # by subtracting the date value and multiplying by 24.
        time = (mjd - int(mjd[0])) * 24

        # Interpolate the x, y, z values for the keyframes.
        # Here we assume that the movement between two snapshots is linear,
        # which is not entirely correct, but good enough for our purposes.
        x = np.interp(keyframes, time, x)
        y = np.interp(keyframes, time, y)
        z = np.interp(keyframes, time, z)

        # Convert cartesian coordinates to spherical coordinates,
        # this works because the origin is at the center of the earth.
        r = np.sqrt(x**2 + y**2 + z**2)
        lat = np.degrees(np.arcsin(z / r))
        lon = np.degrees(np.arctan2(y, x))

        # Calculate the difference towards the previous keyframe,
        # which is used to draw the velocity vector.
        dlat = np.diff(lat)
        dlon = np.diff(lon)
        dlat = np.insert(dlat, 0, 0)
        dlon = np.insert(dlon, 0, 0)

        # Put everything into one dataframe that can be indexed by a keyframe.
        df = pd.DataFrame(
            {
                "x": x,
                "y": y,
                "z": z,
                "lat": lat,
                "lon": lon,
                "dlat": dlat,
                "dlon": dlon,
            }
        )

        return Satellite(name, df)

    position_marker: plt.Line2D
    visibility_marker: plt.Line2D
    velocity_vector: plt.Line2D
    name_label: plt.Text

    def setup_animation(self, ax: plt.Axes):
        is_grace = "grace" in self.name
        color = "deeppink" if self.is_grace else "gold"
        transform = ccrs.Geodetic()

        self.position_marker = ax.plot(
            [],
            [],
            marker="D",
            color=color,
            markersize=5,
            transform=transform,
        )[0]
        self.visibility_marker = ax.plot(
            [],
            [],
            color=color,
            linewidth=0.5,
            transform=transform,
            linestyle="dashed",
        )[0]
        self.velocity_vector = ax.plot(
            [],
            [],
            color=color,
            transform=transform,
        )[0]
        self.name_label = ax.text(
            0,
            0,
            self.name,
            transform=transform,
            fontsize=8,
            ha="left",
            va="center",
            color=color,
            bbox=dict(boxstyle="round", facecolor="black", pad=0.1, alpha=0.5),
        )

    def update_position(self, frame: int) -> list[Artist]:
        lon, lat = self.df.loc[frame, ["lon", "lat"]]
        self.name_label.set_position((lon, lat))
        self.position_marker.set_data(lon, lat)

        # take the last 3 indices, up to frame, and combine their
        # lat and lon into one position array
        velocity_count = 5
        positions = self.df.loc[max(0, frame - velocity_count) : frame, ["lon", "lat"]]
        self.velocity_vector.set_data(positions["lon"], positions["lat"])

        return [self.name_label, self.position_marker, self.velocity_vector]

    def update_visibility(self, frame: int, grace: "Satellite") -> list[Artist]:
        if self == grace:
            return []

        gps_x, gps_y, gps_z, gps_lon, gps_lat = self.df.loc[
            frame, ["x", "y", "z", "lon", "lat"]
        ]
        grace_x, grace_y, grace_z, grace_lon, grace_lat = grace.df.loc[
            frame, ["x", "y", "z", "lon", "lat"]
        ]

        # Figure out whether we are visible to grace.
        # For this, we consider the current xyz positions of both satellites.
        gps_pos = np.array([gps_x, gps_y, gps_z])
        grace_pos = np.array([grace_x, grace_y, grace_z])

        # Calculate two (unit) vectors, one going from GRACE to nadir
        # (which is already the origin of the coordinate system),
        # the other going from the GPS satellite to GRACE.
        e1 = grace_pos
        e1 /= np.linalg.norm(e1)
        e2 = grace_pos - gps_pos
        e2 /= np.linalg.norm(e2)

        # If the angle between these two vectors is greater than 90°,
        # that means that the GPS is "on top" of GRACE and can see it.
        alpha = np.arccos(np.dot(e1, e2))
        is_visible = alpha > np.pi / 2

        if is_visible:
            self.visibility_marker.set_data(
                [grace_lon, gps_lon],
                [grace_lat, gps_lat],
            )
        else:
            self.visibility_marker.set_data([], [])

        return [self.visibility_marker]
