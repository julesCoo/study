from satellite import Satellite
from datetime import datetime
import numpy as np
from ftplib import FTP
import os
from print import print_progress
import matplotlib.pyplot as plt


def load_satellites(date: datetime.date, keyframes: list[float]) -> list[Satellite]:
    """
    Loads all orbit data for a given date into one dataframe.
    Data is automatically downloaded from the FTP if not already present locally.

    :param date: The date for which to load the orbit data.
    :return: A dictionary mapping satellite names to orbit data.
    """

    # Orbits are stored in a directory named after the date
    rel_path = f"orbit/" + date.strftime("%Y-%m-%d")

    # Ensure we have all orbit files in the local directory
    local_path = download_directory(rel_path)

    satellites = []
    for filename in os.listdir(local_path):
        satellite = Satellite.load_from_file(f"{local_path}/{filename}", keyframes)
        satellites.append(satellite)
    return satellites


def load_background_image(date: datetime.date) -> np.ndarray:
    """
    Loads a background image for a given date.

    :param date: The date for which to load the background image.
    :return: The background image as a numpy array.
    """
    month = date.month
    relative_path = f"bluemarble/bluemarble{month:02d}.jpg"
    local_path = download_file(relative_path)
    return plt.imread(local_path)


# Map the directory structure of the FTP server on `ftp_dir` to `local_dir`
ftp_host = "ftp.tugraz.at"
ftp_dir = "/outgoing/ITSG/teaching/2023SS_Informatik2"
local_dir = "data"


def download_file(relative_path: str) -> str:
    """
    Download a single file from the FTP server, if it does not already exist locally.

    :param relative_path: The path to the file relative to the FTP root directory.
    :return: The path to the local file that was downloaded.
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

    :param relative_path: The path to the directory relative to the FTP root directory.
    :return: The path to the local directory that was downloaded.
    """
    ftp_path = f"{ftp_dir}/{relative_path}"
    local_path = f"{local_dir}/{relative_path}"

    # Ensure local directory exists
    print("Syncing orbit files from FTP server...")
    os.makedirs(local_path, exist_ok=True)

    # login to the FTP server
    with FTP(ftp_host) as ftp:
        ftp.login()
        ftp.cwd(ftp_path)
        filenames = ftp.nlst()

        download_list = []
        for filename in filenames:
            local_file = f"{local_path}/{filename}"
            if not os.path.exists(local_file):
                download_list.append(filename)

        if len(download_list) == 0:
            print("All files are up to date.")
        else:
            for i, filename in enumerate(download_list):
                print_progress(f"Downloading {filename}", i, len(download_list))
                with open(f"{local_path}/{filename}", "wb") as fp:
                    ftp.retrbinary("RETR " + filename, fp.write)

    return local_path
