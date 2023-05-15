import argparse
import datetime

import matplotlib.pyplot as plt
from animation import OrbitsAnimation

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

# Parse arguments
args = parser.parse_args()
date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()

# Generate animation
print(f"Generating animation for {date}...")

anim = OrbitsAnimation(
    date=date,
    from_hour=float(args.time[0]),
    to_hour=float(args.time[1]),
    show_satellite_visibility=not args.novisibility,
).start()

# Save animation to file if specified
if args.outfile:
    anim.save(args.outfile, writer="pillow")
    print(f"Saved animation to {args.outfile}.")

# Finally, show animation
print("Displaying animation, close window to exit.")
plt.show()
