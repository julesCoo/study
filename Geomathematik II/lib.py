from sympy import *
import numpy as np
import matplotlib.pyplot as plt


def setup_plot(size=1):
    """
    Setup a 3D plot with equal axes.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_box_aspect([1, 1, 1])
    ax.set_xlim((-size, size))
    ax.set_ylim((-size, size))
    ax.set_zlim((-size, size))


class Surface:
    def __init__(
        self,
        symbols,  # (u,v)
        x,  # x(u,v)
        y,  # y(u,v)
        z,  # z(u,v)
    ):
        u, v = symbols

        f = ImmutableDenseMatrix([x, y, z])

        # Erste Ableitung: Vektoren der Tangentialebene
        f_u = diff(f, u)
        f_v = diff(f, v)

        # Flächennormalenvektor - steht senkrecht auf der Tangentialebene
        z = f_u.cross(f_v)
        z = z / z.norm()
        z = z.replace(Abs, Id)

        # Zweite Ableitung: Krümmungsrichtungen aus der Tangentialebene
        f_uu = diff(f_u, u)
        f_uv = diff(f_u, v)
        f_vv = diff(f_v, v)

        # Erste Fundamentalform - beschreibt innere Geometrie
        E = f_u.dot(f_u)
        F = f_u.dot(f_v)
        G = f_v.dot(f_v)

        # Zweite Fundamentalform
        L = f_uu.dot(z)
        M = f_uv.dot(z)
        N = f_vv.dot(z)

        # Mittlere Krümmung
        H = (E * N - 2 * F * M + G * L) / (2 * (E * G - F**2))
        # Gaußsche Krümmung
        K = (L * N - M**2) / (E * G - F**2)
        # Hauptkrümmungsradien (Achtung Krümmung ist 1/R)
        R1 = 1 / (H + sqrt(H**2 - K))
        R2 = 1 / (H - sqrt(H**2 - K))

        self.u = u
        self.v = v
        self.f = f
        self.f_u = f_u
        self.f_v = f_v
        self.z = z
        self.f_uu = f_uu
        self.f_uv = f_uv
        self.f_vv = f_vv
        self.E = E
        self.F = F
        self.G = G
        self.L = L
        self.M = M
        self.N = N
        self.H = H
        self.K = K
        self.R1 = R1
        self.R2 = R2

    def plot(
        self,
        u_range=(-1, 1, 20),
        v_range=(-1, 1, 20),
        subs={},
        close_surface=False,
        **kwargs,
    ):
        U, V = np.meshgrid(
            np.linspace(*u_range),
            np.linspace(*v_range),
        )

        f = lambdify((self.u, self.v), self.f.subs(subs))

        X, Y, Z = f(U, V).reshape(3, u_range[2], v_range[2])

        ax = plt.gca()
        if close_surface:
            ax.plot_surface(X, Y, Z, **kwargs)
        ax.plot_wireframe(X, Y, Z, **kwargs)


class Curve:
    def __init__(
        self,
        symbols,  # t
        x,  # x(t)
        y,  # y(t)
        z,  # z(t)
    ):
        t = symbols
        f = ImmutableDenseMatrix([x, y, z])

        # Erste Ableitung: Vektor der Tangentialebene
        f_t = diff(f, t)

        # Zweite Ableitung: Krümmungsrichtung aus der Tangentialebene
        f_tt = diff(f_t, t)

        # Normalenvektor
        n = f_tt / f_tt.norm()

        # Krümmung
        k = f_t.norm() / f_t.cross(diff(f_t, t)).norm()

        # Hauptkrümmungsradien (Achtung Krümmung ist 1/R)
        R1 = 1 / k
        R2 = 1 / k

        self.t = t
        self.f = f
        self.f_t = f_t
        self.f_tt = f_tt
        self.n = n
        self.k = k
        self.R1 = R1
        self.R2 = R2

    def plot(
        self,
        t_range=(-1, 1, 20),
        subs={},
    ):
        T = np.linspace(*t_range)

        f = lambdify((self.t), self.f.subs(subs))

        X, Y, Z = f(T).reshape(3, t_range[2])
        plt.gca().plot(X, Y, Z, color="red")


class SurfaceCurve:
    def __init__(
        self,
        surface,  # Surface
        curve,  # Curve
    ):
        v = acos(curve.n.dot(surface.z))

        # Seitenvektor
        s = surface.z.cross(curve.f_t)

        # Normalkrümmung
        # kappa_n = (curve["kappa"] * cos(v))
        kappa_n = curve.f_tt.dot(surface.z)

        # Geodätische Krümmung
        # kappa_g = (curve["kappa"] * sin(v))
        kappa_g = curve.f_tt.dot(s)

        self.surface = surface
        self.curve = curve
        self.v = v
        self.s = s
        self.kappa_n = kappa_n
        self.kappa_g = kappa_g
