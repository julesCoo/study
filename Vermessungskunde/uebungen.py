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

# %% 19 - Ebene Ähnlichkeitstransformation
from lib import YX, CoordinateTransform, to_gon
import numpy as np

P1 = YX(12092.718, 5349728.001)
P2 = YX(14829.446, 5350182.777)

P1_ = YX(55.486, -15.817)
P2_ = YX(-1245.821, -2466.024)
P3_ = YX(-595.168, -1240.921)

# Koordinate Differences
y1, x1 = P1
y2, x2 = P2
eta1, xi1 = P1_
eta2, xi2 = P2_
eta3, xi3 = P3_

dy = y2 - y1
dx = x2 - x1
deta = eta2 - eta1
dxi = xi2 - xi1

d = np.sqrt(dy**2 + dx**2)
d_ = np.sqrt(deta**2 + dxi**2)
mu = d / d_

t = np.arctan2(dy, dx)
t_ = np.arctan2(deta, dxi)
phi = t_ - t
phi_g = to_gon(phi) % 400

y0 = y1 - mu * eta1 * np.cos(phi) + mu * xi1 * np.sin(phi)
x0 = x1 - mu * eta1 * np.sin(phi) - mu * xi1 * np.cos(phi)
print(y0, x0)
y0 = y2 - mu * eta2 * np.cos(phi) + mu * xi2 * np.sin(phi)
x0 = x2 - mu * eta2 * np.sin(phi) - mu * xi2 * np.cos(phi)
print(y0, x0)

y3 = mu * eta3 * np.cos(phi) - mu * xi3 * np.sin(phi) + y0
x3 = mu * eta3 * np.sin(phi) + mu * xi3 * np.cos(phi) + x0
print(y3, x3)

s_x = s_y = s_xy = 0.005
s_eta = s_xi = s_etaxi = 0.001
s_dxy = np.sqrt(2) * s_xy
s_detaxi = np.sqrt(2) * s_etaxi
s_d = s_dxy
s_d_ = s_detaxi

s_mu = np.sqrt((1 / d_) ** 2 * s_d**2 + (d / d_**2) ** 2 * s_d_**2)
s_t = 1 / d * s_dxy
s_t_ = 1 / d_ * s_detaxi
s_phi = np.sqrt(s_t**2 + s_t_**2)

eta, xi = eta2, xi2
s_y0 = np.sqrt(
    1**2 * s_y**2
    + (-eta * np.cos(phi) + xi * np.sin(phi)) ** 2 * s_mu**2
    + (-mu * np.cos(phi)) * s_eta**2
    + (mu * np.sin(phi)) * s_xi**2
    + (mu * eta * np.sin(phi) + mu * xi * np.cos(phi)) ** 2 * s_phi**2
)
s_x0 = np.sqrt(
    1**2 * s_x**2
    + (-eta * np.sin(phi) - xi * np.cos(phi)) ** 2 * s_mu**2
    + (-mu * np.sin(phi)) * s_eta**2
    + (-mu * np.cos(phi)) * s_xi**2
    + (-mu * eta * np.cos(phi) + mu * xi * np.sin(phi)) ** 2 * s_phi**2
)

# %% 22 - Orthogonalaufnahme
import numpy as np
import matplotlib.pyplot as plt
from lib import YX

P1 = YX(19.93, -52.17)
P2 = YX(51.40, 15.66)

dA, lA = (2.18, 5.21)
dB, lB = (3.64, 7.19)
dC, lC = (1.71, 9.04)

vec_line = (P2 - P1).normalize()
vec_ortho = YX(vec_line.x, -vec_line.y)

fpA = P1 + lA * vec_line
PA = fpA + dA * vec_ortho

fpB = P1 + lB * vec_line
PB = fpB + dB * vec_ortho

fpC = P1 + lC * vec_line
PC = fpC + dC * vec_ortho

plt.figure(figsize=(4, 8))
plt.axis("equal")
plt.xlabel("Y [m]")
plt.ylabel("X [m]")

P1.plot()
P2.plot()
P1.plot_to(P2)

fpA.plot_to(PA)
PA.plot(marker="+", label="A")
fpB.plot_to(PB)
PB.plot(marker="+", label="B")
fpC.plot_to(PC)
PC.plot(marker="+", label="C")

# %% 23 - Freie Stationierung
from lib import YX, Polar, bgs, gon, to_gon
import numpy as np
import matplotlib.pyplot as plt

PP1 = YX(-48934.585, 255724.471)
PP2 = YX(-48928.588, 255821.571)

s_1000_PP1 = 44.280
s_1000_PP2 = 53.172
s_1000_N = 60.721

r_1000_PP1 = gon(15.9390)
r_1000_PP2 = gon(223.2140)
r_1000_N = gon(398.6191)

a_1000_PP1_PP2 = to_gon(r_1000_PP2 - r_1000_PP1)
# P1000 = bgs(PP1, PP2, s_1000_PP1, s_1000_PP2)
P1000 = bgs(PP2, PP1, s_1000_PP2, s_1000_PP1)
O1000 = P1000.polar_to(PP1).t - r_1000_PP1
O1000_g = to_gon(O1000)

P1000_O = P1000 + Polar(100, O1000)
N = P1000 + Polar(s_1000_N, O1000 + r_1000_N)

plt.figure(figsize=(2, 6))
plt.xlabel("Y [m]")
plt.ylabel("X [m]")
plt.axis("equal")
PP1.plot(label="PP1")
PP2.plot(label="PP2")
P1000.plot(label="P1000")
P1000.plot_to(PP1)
P1000.plot_to(PP2)
P1000.plot_to(P1000_O, linestyle="--", linewidth=0.5)
P1000.plot_to(N)
N.plot(marker="o", label="N")


# %%
