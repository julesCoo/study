# -*- coding: utf-8 -*-
"""
File: parser.py
Author: Daniel Ebert
Date: 06.06.2023

Description:
    This file configures the command line interface and 
    deals with parsing the arguments into the `Args` class.
"""

import argparse
import datetime
from dataclasses import dataclass
import matplotlib.pyplot as plt


@dataclass
class Args:
    """
    Class to store command line arguments.
    """

    date: datetime.date
    time_range: [float, float]
    show_visibility: bool
    outfile: str
    frames_per_second: int
    animation_speed: float = 1


def parse_arguments():
    """
    Parses command line arguments.

    :return: The parsed arguments.
    """

    parser = argparse.ArgumentParser(
        description="Generates an animated visualization of GRACE satellite visibility "
        + "to the GPS constellation for a single day."
    )
    parser.add_argument(
        "date",
        type=str,
        help="date to visualize (format: YYYY-MM-DD)",
    )
    parser.add_argument(
        "-n",
        "--novisibility",
        action="store_true",
        help="do not show visibility lines",
    )
    parser.add_argument(
        "-o",
        "--outfile",
        type=str,
        help="save animation to this file",
    )
    parser.add_argument(
        "-t",
        "--time",
        type=str,
        nargs=2,
        help="start and end time in hours to limit animation",
        default=["0", "23"],
    )
    parser.add_argument(
        "--fps",
        type=int,
        help="frames per second",
        default=30,
    )
    parser.add_argument(
        "--speed",
        type=float,
        help="hours per second of animation",
        default=1,
    )

    args = parser.parse_args()

    return Args(
        date=datetime.datetime.strptime(args.date, "%Y-%m-%d").date(),
        time_range=[float(args.time[0]), float(args.time[1])],
        show_visibility=not args.novisibility,
        outfile=args.outfile,
        frames_per_second=args.fps,
        animation_speed=args.speed,
    )
