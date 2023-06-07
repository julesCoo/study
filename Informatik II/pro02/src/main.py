# -*- coding: utf-8 -*-
"""
File: main.py
Author: Daniel Ebert
Date: 06.06.2023

Description: 
    This is the main file of the project.
    It provides the entry point and high level program execution.
"""


from animation import create_keyframes, create_animation
from parser import parse_arguments
from loader import load_background_image, load_satellites
import matplotlib.pyplot as plt

"""Configuration by Command Line Arguments"""
args = parse_arguments()

"""Data Loading and Preprocessing"""
keyframes = create_keyframes(
    start_time=args.time_range[0],
    end_time=args.time_range[1],
    time_per_second=args.animation_speed,
    frames_per_second=args.frames_per_second,
)
satellites = load_satellites(
    date=args.date,
    keyframes=keyframes,
)
background_image = load_background_image(
    date=args.date,
)

"""Animation Setup"""
animation = create_animation(
    frames_per_second=args.frames_per_second,
    keyframes=keyframes,
    show_visibility=args.show_visibility,
    satellites=satellites,
    background_image=background_image,
)

"""Output"""
if args.outfile:
    animation.save(args.outfile)
plt.show()
