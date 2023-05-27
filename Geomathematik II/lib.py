from sympy import *
import numpy as np
import matplotlib.pyplot as plt


def setup_plot():
    """
    Setup a 3D plot with equal axes.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_box_aspect([1, 1, 1])


def plot_surface(
    # The function takes (u,v) as input and returns (x,y,z).
    f,
    u_range=(-1, 1),
    v_range=(-1, 1),
    u_count=20,
    v_count=20,
    close_surface=False,
):
    """
    Plot a surface in 3D.
    """

    U, V = np.meshgrid(
        np.linspace(*u_range, u_count),
        np.linspace(*v_range, v_count),
    )
    X, Y, Z = f(U, V).reshape(3, u_count, v_count)

    ax = plt.gca()
    if close_surface:
        ax.plot_surface(X, Y, Z, color="blue", alpha=1.0)
    ax.plot_wireframe(X, Y, Z, color="black", alpha=0.1)


def plot_line(
    # The function takes (t) as input and returns (x,y,z).
    f,
    t_range=(-1, 1),
    t_count=20,
):
    """
    Plot a line in 3D.
    """

    T = np.linspace(*t_range, t_count)
    X, Y, Z = f(T).reshape(3, t_count)
    plt.gca().plot(X, Y, Z, color="red")


def analyse_surface_curve(
    # x is a xyz vector of functions of u and v.
    x,
    # u and v are the symbols used in x.
    u,
    v,
):
    """
    Analyse a surface curve.
    """

    # Länge eines Kurvenstücks
    x_norm = x.norm().simplify()

    # Ableitungen
    x_u = diff(x, u).simplify()
    x_uu = diff(x_u, u).simplify()
    x_v = diff(x, v).simplify()
    x_vv = diff(x_v, v).simplify()
    x_uv = diff(x_u, v).simplify()

    # Flächennormalenvektor
    z = x_u.cross(x_v).simplify()
    z = z / z.norm()

    # Erste Fundamentalform
    E = x_u.dot(x_u).simplify()
    F = x_u.dot(x_v).simplify()
    G = x_v.dot(x_v).simplify()

    # Zweite Fundamentalform
    L = x_uu.dot(z).simplify()
    M = x_uv.dot(z).simplify()
    N = x_vv.dot(z).simplify()

    # Mittlere Krümmung
    H = ((E * N - 2 * F * M + G * L) / (2 * (E * G - F**2))).simplify()

    # Gaußsche Krümmung
    K = ((L * N - M**2) / (E * G - F**2)).simplify()

    # Hauptkrümmungen
    R1 = (H + sqrt(H**2 - K)).simplify()
    R2 = (H - sqrt(H**2 - K)).simplify()

    return {
        "x": x,
        "x_norm": x_norm,
        "x_u": x_u,
        "x_uu": x_uu,
        "x_v": x_v,
        "x_vv": x_vv,
        "x_uv": x_uv,
        "z": z,
        "E": E,
        "F": F,
        "G": G,
        "L": L,
        "M": M,
        "N": N,
        "H": H,
        "K": K,
        "R1": R1,
        "R2": R2,
    }
