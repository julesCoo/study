import numpy as np
import matplotlib.pyplot as plt


def read_signals(fileName):
    """
    Reads the file into a dict of lists.
    The file has multiple lines of the form:
      key=value1,value2,value3,...
    The values are converted to floats if possible.
    """
    with open(fileName, "r") as f:
        data = dict()
        for line in f.read().splitlines():
            key, values_str = line.split("=")
            values = values_str.split(",")

            # if all values for a key are numbers, convert them to floats
            values_are_numbers = all(map(lambda s: s.isdigit(), values))
            if values_are_numbers:
                values = list(map(float, values))

            data[key] = values
        return data


def read_noise(fileName):
    """
    Reads the file into a numpy array (4 x n).
    First column is the time in seconds.
    The other columns are the noise values for the signals.
    """
    return np.loadtxt(fileName)


def plot_signal(axes, signals, noise, index):
    """
    Plot a signal into the given axes.
    `signals` is the dict returned by `read_signals` and contains the rendering configuration.
    `noise` is the numpy array returned by `read_noise` and contains the data to be plotted.
    The plotted signal is a sine wave given as y = A * sin(2*pi*f * t + phi).
    This function is plotted as a line graph, and the individual data points (including noise) are plotted as scatter points.
    """

    A = signals["amplitudes"][index]
    f = signals["frequencies"][index]
    phi = signals["phases"][index]
    color = signals["colors"][index]

    label = f"A = {A:.1f}, f = {f:.1f} Hz, phi = {phi:.1f} deg"

    # Grab the values from the array - index 0 is the time, so we have to add 1 to get the noise values for this signal
    t = noise[:, 0]
    noise_offset = noise[:, index + 1]

    # Calculate the y values corresponding to the time values in t
    y_func = A * np.sin(2 * np.pi * f * t + phi)
    y_noise = y_func + noise_offset

    # Plot the two graphs, but only annotate one of them for the legend
    axes.plot(t, y_func, color=color, label=label)
    axes.scatter(t, y_noise, color=color)


# Read the data
signals = read_signals("signals.txt")
noise = read_noise("noise.txt")

# Setup a figure with a single axis
fig, ax = plt.subplots(1, 1, figsize=(10, 5))
ax.set_xlim(0, 1)
ax.set_xlabel("Time [s]")
ax.grid()

# Plot the three signal into the axis
for i in range(3):
    plot_signal(ax, signals, noise, i)

# Add a legend and save the figure
ax.legend()
fig.savefig("signals.png", dpi=300)
