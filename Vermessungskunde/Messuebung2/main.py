# %%
"Hilfsfunktionen und Konstanten"

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass


def pm200(gon):
    "Berechnet den Komplementärwinkel zu einem Winkel"
    if gon > 200:
        return gon - 200
    else:
        return gon + 200


def pm400(gon):
    "Bringt einen Winkel in den Bereich 0 bis 400 gon"
    if gon > 400:
        return gon - 400
    elif gon < 0:
        return gon + 400
    else:
        return gon


def gon(radians):
    "Konvertiert einen Winkel in Radian in Gon und normalisiert ihn auf 0 bis 400 gon"
    return pm400(radians * 200 / np.pi)


def rad(gon):
    "Konvertiert einen Winkel in Gon in Radiant"
    return gon * np.pi / 200


# 3D-Punkt oder Vektor
@dataclass
class YXH:
    y: float
    x: float
    h: float


# Stand- und Fernpunkte mit bekannten Koordinaten
coordinates = {
    "PF3": YXH(-66786.4983, 5214269.7625, 378.1291),  # Pfeiler 3
    "PF5": YXH(-66769.3684, 5214277.6754, 378.1235),  # Pfeiler 5
    "57-164 T1": YXH(-67692.03, 5213673.65, 421.3),  # Josefskirche
    "73-164 T1": YXH(-66581.29, 5214849.32, 466.89),  # Herz-Jesu-Kirche
    "112-164 M2": YXH(-71883.21, 5217091.97, 804.66),  # Sendeturm Plabutsch
    "26-164 T1": YXH(-71721.95, 5211190.99, 444.76),  # St. Martin
}

# %%
"Daten einlesen und ergänzen"

# Tabelle einlesen
df = pd.read_csv("data.csv")

# Diese Spalten auffüllen (forward fill)
df["Beobachter"].ffill(inplace=True)
df["Instrumentenhöhe [m]"].ffill(inplace=True)
df["Standpunkt"].ffill(inplace=True)
df["Satz"].ffill(inplace=True)
df["Zielpunkt"].ffill(inplace=True)

# %%
"Punktnummern in Koordinaten umwandeln"

sp = df["Standpunkt"].apply(lambda x: coordinates[x])
sp_x = sp.apply(lambda x: x.x)
sp_y = sp.apply(lambda x: x.y)
sp_h = sp.apply(lambda x: x.h) + df["Instrumentenhöhe [m]"]

zp = df["Zielpunkt"].apply(lambda x: coordinates.get(x, None))
zp.dropna(inplace=True)
zp_x = zp.apply(lambda x: x.x)
zp_y = zp.apply(lambda x: x.y)
zp_z = zp.apply(lambda x: x.h)

dx = zp_x - sp_x
dy = zp_y - sp_y
dxy = np.sqrt(dx**2 + dy**2)
dh = zp_z - sp_h

df["Standpunkt X [m]"] = sp_x
df["Standpunkt Y [m]"] = sp_y
df["Standpunkt H [m]"] = sp_h
df["Zielpunkt X [m]"] = zp_x
df["Zielpunkt Y [m]"] = zp_y
df["Zielpunkt H [m]"] = zp_z
df["dX [m]"] = dx
df["dY [m]"] = dy
df["dXY [m]"] = dxy
df["dH [m]"] = dh

# %%
"Atmosphäre interpolieren und Korrekturfaktor berechnen"

# Nach Kreislage sortieren, sodass die Daten in zeitlicher Abfolge sind
# (anders als auf dem Datenblatt, wo Kreislage 1 und 2 direkt aufeinander folgen)
# Jetzt wo die Daten so sortiert sind, können wir eine Zeit-Spalte hinzufügen,
# die einfach linear von 0 bis 1 geht (zum Sortieren/Darstellen über die Zeit)
df.sort_values(by=["Beobachter", "Satz", "Kreislage"], inplace=True)
df["Zeit"] = np.linspace(0, 1, len(df))

# Jetzt kann man die Wetterdaten entlang der Zeitachse interpolieren
# (anhand der Messungen vor und nach jedem Satz)
df["Temp [°C]"].interpolate(method="linear", inplace=True)
df["Luftdruck [hPa]"].interpolate(method="linear", inplace=True)
df["Luftfeuchte [%]"].interpolate(method="linear", inplace=True)

# Mit den Wetterdaten kann man die atmosphärische Korrektion berechnen
p = df["Luftdruck [hPa]"]
t = df["Temp [°C]"]
h = df["Luftfeuchte [%]"]
alpha = 1 / 273.15
x = (7.5 * t) / (237.3 + t) + 0.7857
df["Atmosphärische Korrektion [ppm]"] = 286.34 - (
    ((0.29525 * p) - (4.126e-4 * h)) / (1 + alpha * t) * 10**x
)

# Anschließend reine Wetter-Zeilen löschen, und nur die Zeilen mit Polar-
# Messungen behalten.
df.dropna(subset=["R [gon]"], inplace=True)
df.reset_index(drop=True, inplace=True)

# Zur Kontrolle nochmal plotten, der Trennstrich entspricht dem Beobachterwechsel
# fig, axes = plt.subplots(4, 1, sharex=True)
# df.plot(x="Zeit", y="Temp [°C]", ax=axes[0])
# df.plot(x="Zeit", y="Luftdruck [hPa]", ax=axes[1])
# df.plot(x="Zeit", y="Luftfeuchte [%]", ax=axes[2])
# df.plot(x="Zeit", y="Atmosphärische Korrektion [ppm]", ax=axes[3])
# for ax in axes:
#     ax.axvline(x=0.5, color="k", linestyle="--")

# %%
"Meteorologische Streckenreduktion"

d = df["Schrägdistanz [m]"]
dd = df["Atmosphärische Korrektion [ppm]"]
d_korr = d + (dd * d * 1e-6)

df["korr. Schrägdistanz [m]"] = d_korr

# %%
"Satzausgleichung"

# Jetzt werden die Kreislagen jeweils in eine Messung zusammen gefasst
df.sort_index(inplace=True)

kl1 = df[df["Kreislage"] == 1].reset_index(drop=True)
kl2 = df[df["Kreislage"] == 2].reset_index(drop=True)

# Neues DataFrame anlegen und nur mehr einige Spalten übernehmen.
# (Wetter brauchen wir nicht mehr da Distanz schon korrigiert ist)
df = kl2.copy()
df.drop(columns=["Kreislage"], inplace=True)

R1 = kl1["R [gon]"]
R2 = kl2["R [gon]"]
zeta1 = kl1["zeta [gon]"]
zeta2 = kl2["zeta [gon]"]
dist1 = kl1["korr. Schrägdistanz [m]"]
dist2 = kl2["korr. Schrägdistanz [m]"]


def mean_R(R1, R2):
    if R1 < R2:
        return (R1 + R2 - 200) / 2
    else:
        return (R1 + R2 + 200) / 2


df["R1 [gon]"] = R1
df["R2 [gon]"] = R2
df["R [gon]"] = df.apply(lambda row: mean_R(row["R1 [gon]"], row["R2 [gon]"]), axis=1)
df["c [cc]"] = 1 / 2 * (R2.apply(pm200) - R1) * 1e4

df["zeta1 [gon]"] = zeta1
df["zeta2 [gon]"] = zeta2
df["zeta [gon]"] = 1 / 2 * (400 + (zeta1 - zeta2))
df["i [cc]"] = 1 / 2 * (400 - (zeta1 + zeta2)) * 1e4

# ?? Nicht sicher ob wir so die Distanz mitteln können
df["korr. Schrägdistanz [m]"] = 1 / 2 * (dist1 + dist2)


# ! TODO Ausreißerkontrolle

# %%
"Trigonometrische Höhenübertragung"

# Die gemessene (und korrigierte) Schrägdistanz zum Prisma setzt sich zusammen aus
# horizontaler Distanz und Höhendifferenz.
d = df["korr. Schrägdistanz [m]"]
zeta = df["zeta [gon]"]
sp_h = df["Standpunkt H [m]"]

# Zenitwinkel in Höhenwinkel umrechnen
alpha = (100 - zeta).apply(rad)

s_hor = d * np.cos(alpha)
dh = d * np.sin(alpha)

df["s_hor [m]"] = s_hor
df["dH [m]"].fillna(dh, inplace=True)
df["Zielpunkt H [m]"].fillna(sp_h + dh, inplace=True)

# %%
"Geometrische Streckenkorrektur"

sp_h = df["Standpunkt H [m]"]
zp_h = df["Zielpunkt H [m]"]
H = (sp_h + zp_h) / 2  # mittlere Projekthöhe
R = 6371000  # Erdradius

# Strecke reduzieren
s_ell = (1 - H / R) * s_hor
df["s_ell [m]"] = s_ell

print(f"Horizontalstrecke [m] zur Kontrolle")
print(s_hor.dropna())

# %%
"Gauß-Krüger-Reduktion"

# Hier brauchen wir die mittlere Y-Koordinate, kennen aber nur
# die vom Standpunkt. Denke aber das macht bei der kurzen Distanz
# keinen entscheidenden Unterschied.
y = df["Standpunkt Y [m]"]

s_gk = (1 + y**2 / (2 * R**2)) * s_ell
df["s_GK [m]"] = s_gk

# %%
"Orientierungen berechnen"

dx = df["dX [m]"]
dy = df["dY [m]"]
R = df["R [gon]"]

t = np.arctan2(dy, dx).apply(gon)
O = (t - R).apply(pm400)

df["t [gon]"] = t
df["O [gon]"] = O

# Berechnete Orientierungen plotten, aber getrennt für beide Beobachter, da
# die y-Werte nicht vergleichbar sind.
fig, axes = plt.subplots(2, 1, sharex=True)
df[df["Beobachter"] == "Ebert"].plot(x="Zeit", y="O [gon]", ax=axes[0], kind="scatter")
df[df["Beobachter"] == "Medl"].plot(x="Zeit", y="O [gon]", ax=axes[1], kind="scatter")
for ax in axes:
    ax.yaxis.get_major_formatter().useOffset = False

# %%
"Orientierung mitteln und fehlende Azimuthe ergänzen"

# Mittelwert der Orientierungen pro Beobachter bilden
O = df.groupby("Beobachter")["O [gon]"].mean()

# Wo die Orientierung fehlt, mit dem Mittelwert ergänzen
df["O [gon]"].fillna(df["Beobachter"].map(O), inplace=True)

# Wo die Richtung fehlt, mit der Formel t=R+O ergänzen
df["t [gon]"].fillna((df["R [gon]"] + df["O [gon]"]).apply(pm400), inplace=True)

# %%
"Polarpunktberechnung für Prisma-Zielpunkte"

df_prisma = df[df["Zielpunkt"] == "41"]

sp_x = df_prisma["Standpunkt X [m]"]
sp_y = df_prisma["Standpunkt Y [m]"]
sp_h = df_prisma["Standpunkt H [m]"]

s_GK = df_prisma["s_GK [m]"]
dh = df_prisma["dH [m]"]
t = df_prisma["t [gon]"].apply(rad)

dx = s_GK * np.cos(t)
dy = s_GK * np.sin(t)

zp_x = sp_x + dx
zp_y = sp_y + dy
zp_h = sp_h + dh

df["dX [m]"].fillna(dx, inplace=True)
df["dY [m]"].fillna(dy, inplace=True)
df["Zielpunkt X [m]"].fillna(zp_x, inplace=True)
df["Zielpunkt Y [m]"].fillna(zp_y, inplace=True)
df["Zielpunkt H [m]"].fillna(zp_h, inplace=True)

# Für jeden Beobachter separat ausgeben:
xs, ys, hs = [], [], []
for beobachter in ["Ebert", "Medl"]:
    df_prisma = df[(df["Zielpunkt"] == "41") & (df["Beobachter"] == beobachter)]
    x = df_prisma["Zielpunkt X [m]"]
    y = df_prisma["Zielpunkt Y [m]"]
    h = df_prisma["Zielpunkt H [m]"]

    x_mean, x_std = x.mean(), x.std(ddof=1)
    y_mean, y_std = y.mean(), y.std(ddof=1)
    h_mean, h_std = h.mean(), h.std(ddof=1)

    print(f"Beobachter: {beobachter}")
    print(f"X: {x_mean:.3f} m +- {1000*x_std:.0f} mm")
    print(f"Y: {y_mean:.3f} m +- {1000*y_std:.0f} mm")
    print(f"H: {h_mean:.3f} m +- {1000*h_std:.0f} mm")
    print()

    xs.append(x_mean)
    ys.append(y_mean)
    hs.append(h_mean)

print("Abweichung der Mittelwerte:")
print(f"X: {1000*np.diff(xs)[0]:.0f} mm")
print(f"Y: {1000*np.diff(ys)[0]:.0f} mm")
print(f"H: {1000*np.diff(hs)[0]:.0f} mm")


# %%
