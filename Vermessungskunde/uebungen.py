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
        return f"{self.gon:.5f}g"

    def __add__(self, other):
        return Angle(self.rad + other.rad)

    def __sub__(self, other):
        return Angle(self.rad - other.rad)

    def sin(self):
        return np.sin(self.rad)

    def cos(self):
        return np.cos(self.rad)

    def tan(self):
        return np.tan(self.rad)

    def cot(self):
        return 1 / np.tan(self.rad)


def rad(x):
    return Angle(x)


def deg(deg, min=0, sec=0):
    return Angle.from_deg(deg, min, sec)


def gon(gon, c=0, cc=0):
    return Angle.from_gon(gon, c, cc)


class YX:
    y: float
    x: float

    def __init__(self, y: float, x: float):
        self.y = y
        self.x = x

    def to_polar(self):
        s = np.sqrt(self.y**2 + self.x**2)
        t = rad(np.arctan2(self.y, self.x))
        return Polar(s, t)

    def __str__(self) -> str:
        return f"YX(y={self.y}m, x={self.x}m)"

    def __add__(self, other):
        return YX(self.y + other.y, self.x + other.x)

    def __sub__(self, other):
        return YX(self.y - other.y, self.x - other.x)


class Polar:
    dist: float
    azimuth: Angle

    def __init__(self, dist: float, azimuth: Angle):
        self.dist = dist
        self.azimuth = azimuth

    def to_yx(self):
        y = self.dist * np.sin(self.azimuth)
        x = self.dist * np.cos(self.azimuth)
        return YX(y, x)

    def __str__(self) -> str:
        return f"Polar({self.dist:.5f}m, {self.azimuth})"


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
print(Polar(201.344, gon(381.720)).to_yx())

# %% 6- Teilkreisorientierung
P10 = YX(-66182.18, 5215829.07)
P11 = YX(-66182.18, 5215834.07)
P14 = YX(-66136.44, 5215849.28)
P71 = YX(-66501.20, 5215444.07)

print("10->11", P11 - P10)
print("10->14", P14 - P10)
print("10->71", P71 - P10)

# Oriented angles from P10 (Theodolite) to P11, P14, P71
a_10_11 = (P11 - P10).to_polar().azimuth
a_10_14 = (P14 - P10).to_polar().azimuth
a_10_71 = (P71 - P10).to_polar().azimuth
print("a(10->11)", a_10_11)
print("a(10->14)", a_10_14)
print("a(10->71)", a_10_71)

# Unoriented angles
r_10_11 = gon(204.7964)
r_10_14 = gon(278.3129)
r_10_71 = gon(48.8534)


print(
    a_10_11 - r_10_11,
    a_10_14 - r_10_14,
    a_10_71 - r_10_71,
)

# %% 7 - Abschätzung: Auswirkung von Koordinatenfehlern
dx = 0.5
dy = 0.5


def d_phi(yx: YX):
    x = yx.x
    y = yx.y
    return rad(abs(x / (x**2 + y**2) * dy - y / (x**2 + y**2) * dx))


print(d_phi(P11 - P10))
print(d_phi(P14 - P10))
print(d_phi(P71 - P10))

# %% 8 - Polarpunktberechnung

NA = P10 + Polar(172.081, gon(87.8787)).to_yx()
NB = P10 + Polar(19.994, gon(207.4406)).to_yx()
print(NA)
print(NB)

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
