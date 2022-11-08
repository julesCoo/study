from lib.vector import Vec2

"""
Ein Klotz der Masse 800 g wird auf einer im Bild gezeigten Oberfläche mit gleichbleibender Geschwindigkeit 
v verschoben. Zwischen r0 und r1 und zwischen r1 und r2 sei die Oberfläche eine geneigte Ebene.
Für diese Verschiebung bewegen wir den Klotz mit einer Kraft parallel zur Oberfläche.
"""

mass = 0.8

r0 = Vec2(0, 0)
r1 = Vec2(1.5, 2.5)
r2 = Vec2(2.3, 2)


def work(ra: Vec2, rb: Vec2):
    dr = rb - ra
    dist = dr.normalize()
    force = dr.y * 9.81 * mass
    return force * dist


print(work(r0, r1) + work(r1, r2))
