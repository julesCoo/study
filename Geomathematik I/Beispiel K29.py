#%%
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from math import degrees, radians
from libgeo import from_deg
from libsphere import SphereTriangle, SphereCoords, ha1, ha2, plot_line, plot_point


r = 6370  # km

# ship moves from a to b
A = SphereCoords(from_deg(2, 28), from_deg(-30, 12))
B = SphereCoords(from_deg(-3, 46), from_deg(-32, 27))

# ship passes p1 and p2
lam1 = from_deg(-30, 30)
phi2 = from_deg(-2, 45)

# Calculate the azimuth of the ship's direction at A
_, aAB, _ = ha2(A, B)

# The azimuth is an angle in a pole triangle.
# We also know the pole distances of A and P2.

T = SphereTriangle.wsw(
    alpha=A.lam - lam1,
    beta=radians(360) - aAB,
    c=radians(90) - A.phi,
)
P1, _ = ha1(A, T.a, aAB)

T, _ = SphereTriangle.ssw(
    a=radians(90) - phi2,
    c=radians(90) - A.phi,
    alpha=radians(360) - aAB,
)
P2, _ = ha1(A, T.b, aAB)

dist, _, _ = ha2(P1, P2)
dist *= r

print(f"P1: {P1}")
print(f"P2: {P2}")
print(f"Distance: {dist} km")

ax = plt.subplot(projection=ccrs.Mercator())
ax.stock_img()
ax.set_extent([-40, -25, -6, 4])
ax.coastlines(alpha=1)
gl = ax.gridlines(
    crs=ccrs.PlateCarree(),
    draw_labels=True,
    # xlocs=[0, 4],
    # ylocs=[50, 54, 58],
    linewidth=0.25,
)
gl.top_labels = False
gl.right_labels = False

plot_line(A, B, color="black")

plot_point(A, "A", marker="^", color="black")
plot_point(B, "B", marker="^", color="black")

plot_line(SphereCoords(-6, lam1), SphereCoords(4, lam1), color="red")
plot_point(P1, "P1", marker="o", color="red")

plot_line(SphereCoords(phi2, -34), SphereCoords(phi2, -30), color="green")
plot_point(P2, "P2", marker="o", color="green")


plt.show()

# SphereTriangle.ssw(
#     a=degrees(90) - phi2,
#     c=degrees(90) - A.phi,
#     alpha=degrees(360) - aAB,
# )


# calculate the azimuth

# %%
