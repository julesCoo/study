import os
import datetime
from ftplib import FTP
from Satellite import Satellite
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

# Map the directory structure of the FTP server on `ftp_dir` to `local_dir`
ftp_host = "ftp.tugraz.at"
ftp_dir = "/outgoing/ITSG/teaching/2023SS_Informatik2"
local_dir = "data"


def date_to_path(date: datetime.date) -> str:
    """
    Converts date to the relative path where orbit files for that date are stored.
    """
    dirname = date.strftime("%Y-%m-%d")
    return f"orbit/{dirname}"


def download_file(relative_path: str) -> str:
    """
    Download a single file, if it does not exist locally.
    Returns the path to the local file.
    """
    ftp_path = f"{ftp_dir}/{relative_path}"
    local_path = f"{local_dir}/{relative_path}"

    # Do not download if file already exists
    if os.path.exists(local_path):
        return local_path

    # Ensure local directory exists
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    # login to the FTP server
    with FTP(ftp_host) as ftp:
        ftp.login()
        with open(local_path, "wb") as fp:
            ftp.retrbinary("RETR " + ftp_path, fp.write)

    return local_path


def download_directory(relative_path: str) -> str:
    """
    Downloads all files in a given directory from the FTP.
    Files that already exist locally are not downloaded again.

    Returns the path to the local directory.
    """
    ftp_path = f"{ftp_dir}/{relative_path}"
    local_path = f"{local_dir}/{relative_path}"

    # Ensure local directory exists
    os.makedirs(local_path, exist_ok=True)

    # login to the FTP server
    with FTP(ftp_host) as ftp:
        ftp.login()
        ftp.cwd(ftp_path)
        filenames = ftp.nlst()

        for filename in filenames:
            local_file = f"{local_path}/{filename}"
            if os.path.exists(local_file):
                # File already exists, skip download
                continue

            # Download file
            print(f"Downloading {filename}...")
            with open(local_file, "wb") as fp:
                ftp.retrbinary("RETR " + filename, fp.write)

    return local_path


def load_satellites(date: datetime.date) -> list[Satellite]:
    """
    Loads all orbit data for a given date into one dataframe.
    Data is automatically downloaded from the FTP if not already present locally.
    """
    # Ensure we have all orbit files in the local directory
    rel_path = date_to_path(date)
    local_path = download_directory(rel_path)

    satellites = []
    for filename in os.listdir(local_path):
        filepath = f"{local_path}/{filename}"
        satellite = Satellite.load_from_file(filepath)
        satellites.append(satellite)
    return satellites


def load_background_image(date: datetime.date) -> np.ndarray:
    """Loads a background image for a given date."""
    month = date.month
    relative_path = f"bluemarble/bluemarble{month:02d}.jpg"
    local_path = download_file(relative_path)
    return plt.imread(local_path)
