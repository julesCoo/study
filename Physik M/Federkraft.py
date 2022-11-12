from lib.calculus import integrate

"""
Eine Kugel mit der Masse 8 kg ist an einer nicht linearen Feder angebracht. Die Federkraft ist F_Feder = -9x|x| N.
x ist hierbei die Auslenkung der Feder in Metern. Die Feder wird 2 cm von ihrer Ruheposition ausgelenkt.

(a) Wie viel Energie wird benötigt, um die Feder von x = 0 bis x = 2 cm zu dehnen?

Die Masse wird von x=2 cm aus dem Ruhezustand losgelassen. Wenn die Feder versucht sich wieder
in ihre Ruheposition zurück zu bewegen wirkt auf die Masse eine Reibungskraft, die der Bewegungsrichtung
entgegensetzt ist: F_drag = -5 (v_x)^3 N.

Welche Differentialgleichung muss gelöst werden um die Bewegung der Kugel bestimmen zu können?
"""

mass = 4

def F_Feder(x):
    return -4 * x * abs(x)


min_x = 0
max_x = 0.02

energy = -integrate(F_Feder, min_x, max_x)
print(energy)


def F_drag(v_x):
    return -5 * v_x**3

