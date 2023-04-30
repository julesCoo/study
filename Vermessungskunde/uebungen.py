# %% 1 - Gebräuchliche Winkelmaße
w1 = deg(124, 30, 30)
w2 = gon(124, 30, 30)

print(w1.rad, w1.deg, w1.dms, w1.gon, w1.gonccc)
print(w2.rad, w2.deg, w2.dms, w2.gon, w2.gonccc)

# %%  2 - Abschätzung: Vertikalwinkelmessung
s = 50
a = gon(0.7 * 1e-3)
h = s * tan(a.rad)
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
z = gon(50)
dz = gon(2e-3)

# Differentiale
df_ds = z.cot()
df_dz = -s / (z.sin() ** 2)

# Totales Differential
dh = abs(df_ds * ds) + abs(df_dz * dz.rad)

# Varianzfortpflanzung
sh = sqrt(df_ds**2 * ds**2 + df_dz**2 * dz.rad**2)
print("dh=", dh * 1000, "mm")
print("sh=", sh * 1000, "mm")
# %%


s = np.linspace(0, 100, 100)
z = np.linspace(50, 150, 100)
s, z = np.meshgrid(s, z)
df_ds = 1 / tan(z)
df_dz = -s / (sin(z) ** 2)
sh = sqrt(df_ds**2 * ds**2 + df_dz**2 * dz.rad**2)

plt.xlabel("s [m]")
plt.ylabel("$\\zeta$ [gon]")
cnt = plt.contourf(s, z, sh)
plt.colorbar(cnt, label="$s_h$ [m]")
plt.savefig("Varianzfortpflanzung.png")

# %% 13 - Varianzfortpflanzung bei Koordinatenrechnung

t = gon(381.720).rad
st = gon(1.5e-3).rad

s = 201.344
ss = 5e-3

sx = sqrt(sin(t) ** 2 * ss**2 + (s * cos(t)) ** 2 * st**2)
sy = sqrt(cos(t) ** 2 * ss**2 + (-s * sin(t)) ** 2 * st**2)
print("sx=", sx * 1000, "mm", "sy=", sy * 1000, "mm")

# %% 14 - Teilkreisorientierung

y = 0
y = 45.74
y = -319.02
sy = sqrt(2) * 0.01

x = 5
x = 21.01
x = -385.0
sx = sqrt(2) * 0.01

# R = gon(278.3129).rad
sR = gon(1e-3).rad

sO = sqrt(
    (x / (x**2 + y**2)) ** 2 * sy**2
    + (-y / (x**2 + y**2)) ** 2 * sx**2
    + (-1) ** 2 * sR**2
)
print(gon(sO).gon * 1000, "mgon")

# %% 15 - Polarpunktberechnung

d = 172.081
d = 19.994
sd = 5e-3

R = gon(87.8787).rad
R = gon(207.4406).rad
sR = gon(1e-3).rad

sx10 = 0.01
sy10 = 0.01

sy = sqrt(sin(R) ** 2 * sd**2 + (d * cos(R)) ** 2 * sR**2 + sy10**2)
sx = sqrt(cos(R) ** 2 * sd**2 + (-d * sin(R)) ** 2 * sR**2 + sx10**2)
print("sx=", sx * 1000, "mm", "sy=", sy * 1000, "mm")

# %% 16 - Allgemeiner Richtungsschnitt
from importlib import reload
import lib

reload(lib)


import numpy as np
import matplotlib.pyplot as plt
from lib import YX, Polar, gon, to_gon, vws

p_130 = YX(-60751, 5207637)  # Anfangspunkt
p_136 = YX(-61001, 5208713)  # Endpunkt
p_1 = YX(-60176, 5207125)  # Kirche Matrei
p_14 = YX(-59252, 5212812)  # Nüssingkogel

R_130_to_1 = gon(144.314)
R_130_to_14 = gon(15.949)
R_130_to_unknown = gon(42.715)
R_136_to_1 = gon(166.497)
R_136_to_14 = gon(22.675)
R_136_to_unknown = gon(60.936)

O_130 = np.mean(
    [
        p_130.polar_to(p_1).t - R_130_to_1,
        p_130.polar_to(p_14).t - R_130_to_14,
    ]
)

O_136 = np.mean(
    [
        p_136.polar_to(p_1).t - R_136_to_1,
        p_136.polar_to(p_14).t - R_136_to_14,
    ]
)

p_unknown = vws(
    p_130,
    p_136,
    O_130 + R_130_to_unknown,
    O_136 + R_136_to_unknown,
)

print(to_gon(O_130 + R_130_to_unknown))
print(to_gon(O_136 + R_136_to_unknown))


p_1.plot("1-152")
p_14.plot("14-152")
p_unknown.plot("unknown")

p_130.plot("130-152", color="red")
p_130.plot_to(p_1, color="red")
p_130.plot_to(p_14, color="red")
p_130.plot_to(p_unknown, color="red")

p_136.plot("136-152", color="green")
p_136.plot_to(p_1, color="green")
p_136.plot_to(p_14, color="green")
p_136.plot_to(p_unknown, color="green")

print("O_130=", to_gon(O_130), "gon")
print("O_136=", to_gon(O_136), "gon")
print(p_unknown)

plt.ticklabel_format(useOffset=True, style="plain", axis="both")
plt.ylabel("x [m]")
plt.xlabel("y [m]")
plt.subplots_adjust(left=0.15, right=0.9, top=0.9, bottom=0.1)
plt.savefig("AllgemeinerRichtungsschnitt.png")

# %% 17 - Nivelliertest
import numpy as np

meas_back = np.array(
    [1.767, 1.691, 1.734, 1.722, 1.759, 1.753, 1.722, 1.675, 1.756, 1.718]
)
meas_front = np.array(
    [1.275, 1.200, 1.235, 1.228, 1.265, 1.252, 1.219, 1.180, 1.256, 1.222]
)

diff = meas_front - meas_back
mean = np.mean(diff)
std = np.std(diff, ddof=1)
print("mean=", mean, "m")
print("std=", std * 1000, "mm")

# %% 18 - Gruppenweise Mittelbildung (gewichtetes Mittel)

mean_back = np.mean(meas_back)
std_back = np.std(meas_back, ddof=1)
mean_front = np.mean(meas_front)
std_front = np.std(meas_front, ddof=1)

mean = mean_front - mean_back
std = np.sqrt(std_back**2 + std_front**2)

print("mean(front)= ", mean_front, "m")
print("std(front)= ", std_front * 1000, "mm")

print("mean(back)= ", mean_back, "m")
print("std(back)= ", std_back * 1000, "mm")

print("mean=", mean, "m")
print("std=", std * 1000, "mm")

for i in range(10):
    left = (-30, meas_back[i])
    right = (30, meas_front[i])
    c = plt.get_cmap("tab10")(i)
    plt.scatter(left[0], left[1], c=c)
    plt.scatter(right[0], right[1], c=c)
    plt.plot([left[0], right[0]], [left[1], right[1]], c=c)

plt.xlabel("Distanz [m]")
plt.ylabel("Höhe [m]")
plt.savefig("GruppenweiseMittelbildung.png")

# %%
