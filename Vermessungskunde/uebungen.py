# %%
from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt


# Universal Angle converter
class Angle:
    rad: float
    deg: float
    gon: float
    dms: tuple[int, int, float]
    gonccc: tuple[int, int, float]

    def __init__(self, rad: float):
        while rad > 2 * np.pi:
            rad -= 2 * np.pi
        while rad < 0:
            rad += 2 * np.pi

        self.rad = rad
        self.deg = rad / np.pi * 180
        self.gon = rad / np.pi * 200

        deg = int(self.deg)
        min = int((self.deg - deg) * 60)
        sec = (self.deg - deg - min / 60) * 3600
        self.dms = (deg, min, sec)

        gon = int(self.gon)
        c = int((self.gon - gon) * 100)
        cc = (self.gon - gon - c / 100) * 10000
        self.gonccc = (gon, c, cc)

    @classmethod
    def from_deg(cls, deg, min, sec):
        deg += min / 60
        deg += sec / 3600
        return cls(deg / 180 * np.pi)

    @classmethod
    def from_gon(cls, gon, c, cc):
        gon += c / 100
        gon += cc / 10000
        return cls(gon / 200 * np.pi)

    def __repr__(self):
        return f"{self.gon}g"

    def __add__(self, other):
        return Angle(self.rad + other.rad)

    def __sub__(self, other):
        return Angle(self.rad - other.rad)


def rad(x):
    return Angle(x)


def deg(deg, min=0, sec=0):
    return Angle.from_deg(deg, min, sec)


def gon(gon, c=0, cc=0):
    return Angle.from_gon(gon, c, cc)


# %% 1 - Gebräuchliche Winkelmaße

w1 = deg(124, 30, 30)
w2 = gon(124, 30, 30)

print(w1.rad, w1.deg, w1.dms, w1.gon, w1.gonccc)
print(w2.rad, w2.deg, w2.dms, w2.gon, w2.gonccc)

# %%  2 - Abschätzung: Vertikalwinkelmessung
s = 50
a = gon(0.7 * 1e-3)
h = s * np.tan(a.rad)
print(h * 1000, "mm")

# %% - 3 - Abschätzung: Nivellement aus der Mitte
da = deg(0, 0, 10)
dy = 0.1e-3
dx = dy / (2 * da.rad)
print(f"dx: {dx:f} m")
print(f"dy: {dy:f} m")
print(f"da: {da.rad:f} rad")

# %% 4 - Abschätzung: Europabrücke - Erdkrümmungseinfluss
r = 6370000
h = 190

d1 = 200
d2 = d1 / (r + h) * r

print(f"{d2=} m")
print(f"{d1-d2=} m")


# %% 5 - Umrechnung zwischen Polarkoordinaten und rechtwinkeligen Koordinaten
def yx_to_polar(y: float, x: float):
    s = (x**2 + y**2) ** 0.5
    t = np.atan2(y, x)
    return s, t


def polar_to_yx(s: float, t: Angle):
    x = s * np.cos(t.rad)
    y = s * np.sin(t.rad)
    return x, y


AB = (201.344, gon(381.720))
y, x = polar_to_yx(*AB)
print(f"{y=} m")
print(f"{x=} m")


# %% Teilkreisorientierung
YX = namedtuple("YX", "y x")
Polar = namedtuple("Polar", "s t")


def azimuth_between(p1: YX, p2: YX):
    dy = p2.y - p1.y
    dx = p2.x - p1.x
    return rad(np.arctan2(dy, dx))


# (y,x)
P10 = (-66182.18, 5215829.07)
P11 = (-66182.18, 5215834.07)
P14 = (-66136.44, 5215849.28)
P71 = (-66501.20, 5215444.07)

r_10_11 = gon(204.7964)
r_10_14 = gon(278.3129)
r_10_71 = gon(48.8534)

a_10_11 = azimuth_between(P10, P11)
a_10_14 = azimuth_between(P10, P14)
a_10_71 = azimuth_between(P10, P71)

print(
    r_10_11 - a_10_11,
    r_10_14 - a_10_14,
    r_10_71 - a_10_71,
)


# %% Trigonometrische Höhenübertragung

# Horizontale Distanz vom Theodoliten zum Messpunkt (in m)
s = 100
ds = 5e-3

# Zenitwinkel (in gon)
z = 50
dz = 2e-3

# Differentiale
df_ds = gcot(z)
df_dz = -s / (gsin(z) ** 2)

# Totales Differential
dh = df_ds * ds + df_dz * dz

# Varianzfortpflanzung
sh = np.sqrt(df_ds**2 * ds**2 + df_dz**2 * dz**2)
print(dh, sh, sh**2)
# %%


s = np.linspace(0, 100, 100)
z = np.linspace(50, 150, 100)
s, z = np.meshgrid(s, z)
df_ds = gcot(z)
df_dz = -s / (gsin(z) ** 2)
sh = np.sqrt(df_ds**2 * ds**2 + df_dz**2 * dz**2)

plt.xlabel("s [m]")
plt.ylabel("$\\zeta$ [gon]")
cnt = plt.contourf(s, z, sh)
plt.colorbar(cnt, label="$s_h$ [m]")
plt.savefig("Varianzfortpflanzung.png")

# %%
