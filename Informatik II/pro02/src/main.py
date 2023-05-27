from animation import create_keyframes, create_animation
from parser import parse_arguments
from loader import load_background_image, load_satellites
import matplotlib.pyplot as plt

"""Dynamic Configuration"""
args = parse_arguments()

"""Data Loading and Preprocessing"""
keyframes = create_keyframes(
    *args.time_range,
    time_per_second=args.animation_speed,
    frames_per_second=args.frames_per_second,
)
satellites = load_satellites(args.date, keyframes)
background_image = load_background_image(args.date)

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
