from lib.calculus import integrate

"""
Die Position eines Teilchens ist gegeben durch x = 4t.
Mit t der Zeit in Sekunden. Die Kraft, die auf das Teilchen wirkt ist F = -5 |v| v - 2x.
Hier ist x die Position in Metern und v ist die Geschwindigkeit in m/s.
Wie groß ist die benötigte Arbeit um das Teilchen zwischen der Zeit t = 0 Sekunden und t = 5 Sekunden zu bewegen?
"""


def x(t):
    return 6 * t


# x/dx = 4
v = 6


def F(t):
    force = -5 * abs(v) * v - 7 * x(t)
    return -force


def P(t):
    return F(t) * v


work = integrate(P, 0, 4)
print(work)
