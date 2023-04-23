import os
import gzip
from ftplib import FTP


def download(host: str, directory: str, filename: str, overwrite: bool = False) -> None:
    """
    Download a file from an FTP server.

    :param host: The FTP server host.
    :param directory: The directory on the server containing the file.
    :param filename: The name of the file to download.
    :param overwrite: If True, overwrite the local file if it exists.
    """
    # Only overwrite an existing file if overwrite is True
    if os.path.exists(filename) and not overwrite:
        return

    with FTP(host) as ftp:
        ftp.login()  # anonymous login
        ftp.cwd(directory)
        with open(filename, "wb") as fp:
            ftp.retrbinary("RETR " + filename, fp.write)


def decompress(filename: str) -> None:
    """
    Decompress a gzip file.

    :param filename: The name of the gzip file to decompress.
    :raises ValueError: If the filename does not end with '.gz'.
    """
    if not filename.endswith(".gz"):
        raise ValueError("not a gzip file")

    with gzip.open(filename, "rb") as fp_in:
        filename_out = filename[:-3]  # remove '.gz' from filename
        with open(filename_out, "wb") as fp_out:
            fp_out.write(fp_in.read())
