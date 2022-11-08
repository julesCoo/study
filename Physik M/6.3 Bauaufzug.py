"""
Ein Bauaufzug soll Baumaterial zur Baustelle befördern. Der Aufzug muß in der Lage sein, ein maximales Gewicht von
m = 1674 kg mit einer Geschwindigkeit von v = 0.8 m/s vertikal zu bewegen.
Welche minimale Leistung muß der Aufzug aufbringen?
"""

mass = 1674
velocity = 0.8

# Power = Work / Time
# Work = Force * Distance
# Velocity = Distance / Time
# => Power = Force * Velocity

force = mass * 9.81
power = force * velocity

print(power)
