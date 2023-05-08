import numpy as np
import matplotlib.pyplot as plt


def x(delta, lamda):
    return [
        (4 + np.cos(delta)) * np.cos(lamda),
        (4 + np.cos(delta)) * np.sin(lamda),
        np.sin(delta),
    ]


# derivation of x with respect to delta
def x_delta(delta, lamda):
    return [
        -np.sin(delta) * np.cos(lamda),
        -np.sin(delta) * np.sin(lamda),
        np.cos(delta),
    ]


# derivation of x with respect to lamda
def x_lamda(delta, lamda):
    return [
        -(4 + np.cos(delta)) * np.sin(lamda),
        (4 + np.cos(delta)) * np.cos(lamda),
        0,
    ]


# second derivation of x with respect to delta
def x_delta_delta(delta, lamda):
    return [
        -np.cos(delta) * np.cos(lamda),
        -np.cos(delta) * np.sin(lamda),
        -np.sin(delta),
    ]


# second derivation of x with respect to delta and lamda
def x_delta_lamda(delta, lamda):
    return [
        np.sin(delta) * np.sin(lamda),
        -np.sin(delta) * np.cos(lamda),
        0,
    ]


# second derivation of x with respect to lamda
def x_lamda_lamda(delta, lamda):
    return [
        -(4 + np.cos(delta)) * np.cos(lamda),
        -(4 + np.cos(delta)) * np.sin(lamda),
        0,
    ]


# cross produduct of x_delta and x_lamda (and is normalized)
def z(delta, lamda):
    z = np.cross(x_delta(delta, lamda), x_lamda(delta, lamda))
    return z / np.linalg.norm(z)


deltas, lamdas = np.meshgrid(
    np.linspace(0, 2 * np.pi, 50),
    np.linspace(0, 2 * np.pi, 50),
)
xs = x(deltas, lamdas)

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.plot_wireframe(xs[0], xs[1], xs[2], color="black", alpha=0.1)
ax.set_aspect("equal")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")


def draw_tangent(delta, lamda, vec, **kwargs):
    ax.plot(
        [x(delta, lamda)[0], x(delta, lamda)[0] + vec[0]],
        [x(delta, lamda)[1], x(delta, lamda)[1] + vec[1]],
        [x(delta, lamda)[2], x(delta, lamda)[2] + vec[2]],
        **kwargs,
    )


delta, lamda = np.pi / 3, np.pi / 3
draw_tangent(delta, lamda, x_delta(delta, lamda), color="red")
draw_tangent(delta, lamda, x_lamda(delta, lamda), color="green")
draw_tangent(delta, lamda, z(delta, lamda), color="blue")

draw_tangent(delta, lamda, x_delta_delta(delta, lamda), color="red", linestyle="dashed")
draw_tangent(
    delta, lamda, x_delta_lamda(delta, lamda), color="green", linestyle="dashed"
)
draw_tangent(
    delta, lamda, x_lamda_lamda(delta, lamda), color="blue", linestyle="dashed"
)

plt.show()
