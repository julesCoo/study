import argparse
import datetime
import matplotlib.pyplot as plt

from animation import generate_animation

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
    default=["0", "24"],
)

# Parse arguments
args = parser.parse_args()
date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()


# Generate animation
generate_animation(
    date=date,
    from_time=datetime.time(int(args.time[0])),
    to_time=datetime.time(int(args.time[1])),
    visibility=not args.novisibility,
)

# Save or show animation
if args.outfile:
    plt.savefig(args.outfile)
else:
    plt.show()
