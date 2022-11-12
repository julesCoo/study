import math

"""
Eine Box der Masse 25 kg wird 9 Meter über den Boden geschleift, indem an einem Seil 
mit der Kraft 51 N gezogen wird. Das Seil wird unter einem Winkel von 45° zur Vertikalen gezogen.
Wenn sich die Box bewegt, wandelt die Reibung mechanische Energie in Wärme um.
Wieviel thermische Energie wurde erzeugt nachdem die Box aufgehört hat sich zu bewegen?
"""

mass = 25
distance = 9
force = 51
angle = 45

effective_force = force * math.sin(math.radians(angle))
work = effective_force * distance
energy = work
print("energy = %s J" % energy)
