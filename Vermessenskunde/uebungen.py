# %% Winkelmaße
from math import tau, sin, cos, tan, atan2


def from_gon(g: float, c: float = 0, cc: float = 0) -> float:
    dg = abs(g)
    dg += c / 100
    dg += cc / (100 * 100)
    if g < 0:
        dg *= -1
    return tau * dg / 400


def to_dg(r: float) -> float:
    return r / tau * 400


def to_gccc(r: float) -> tuple[int, int, float]:
    dg = to_dg(r)
    g = int(dg)
    dg -= g
    dg *= 100
    c = int(dg)
    dg -= c
    dg *= 100
    cc = float(dg)
    return g, c, cc


def from_deg(d: float, m: float = 0, s: float = 0) -> float:
    dd = abs(d)
    dd += m / 60
    dd += s / (60 * 60)
    if d < 0:
        dd *= -1
    return tau * dd / 360


def to_dd(r: float) -> float:
    return r / tau * 360


def to_dms(r: float) -> tuple[int, int, float]:
    dd = to_dd(r)
    d = int(dd)
    dd -= d
    dd *= 60
    m = int(dd)
    dd -= m
    dd *= 60
    s = float(dd)
    return d, m, s


w1_rad = from_deg(124, 30, 30)
w1_dd = to_dd(w1_rad)
w1_dms = to_dms(w1_rad)
w1_dg = to_dg(w1_rad)
w1_gccc = to_gccc(w1_rad)

w2_rad = from_gon(124, 30, 30)
w2_dd = to_dd(w2_rad)
w2_dms = to_dms(w2_rad)
w2_dg = to_dg(w2_rad)
w2_gccc = to_gccc(w2_rad)

for value in [
    w1_rad,
    w1_dd,
    w1_dms,
    w1_dg,
    w1_gccc,
    w2_rad,
    w2_dd,
    w2_dms,
    w2_dg,
    w2_gccc,
]:

    def round(x):
        if isinstance(x, float):
            return f"{x:.3f}"
        else:
            return str(x)

    s = "["
    if isinstance(value, tuple):
        s += "("
        s += ",".join([round(v) for v in value])
        s += ")"
    else:
        s += round(value)
    s += "],"
    print(s)


# %% Aufgabe 2

x = 50
angle = from_gon(0.7e-3)
y = x * tan(angle)
print(y)

# %% Aufgabe 3

da = from_deg(0, 0, 10)
dy = 0.1e-3
dx = dy / (2 * da)
print(f"{dx:f} m")
print(f"{dy:f} m")
print(f"{da:f} rad")

# %% Aufgabe 4
r = 6370000
d1 = 200
h = 190

d2 = d1 / (r + h) * r
print(f"{d2=}")
print(f"{d1-d2=}")


# %% Aufgabe 5
def xy_to_polar(x, y):
    s = (x**2 + y**2) ** 0.5
    t = atan2(y, x)
    return s, t


def polar_to_xy(s, t):
    x = s * cos(t)
    y = s * sin(t)
    return x, y


AB = (201.344, from_gon(381.720))
x, y = polar_to_xy(*AB)
print(f"{x=}")
print(f"{y=}")

# %% Aufgabe 6

y10, x10 = -66182.18, 5215829.07
y11, x11 = -66182.18, 5215834.07
y14, x14 = -66136.44, 5215849.28
y71, x71 = -66501.20, 5215444.07

_, t10_11 = xy_to_polar(x11 - x10, y11 - y10)

r10_11 = from_gon(204.7964)
r10_14 = from_gon(278.3129)
r10_71 = from_gon(48.8534)

# %%
