"""
Eine Spannung von 8 V ist zwischen zwei vertikalen Metallplatten, die einen Abstand 
d = 15 cm haben, anlegt. Zur Zeit t = 0, sei ein Elektron genau in der Mitte zwischen 
den Platten und habe keine Geschwindigkeit. Zu welcher Zeit t s wird das Elektron auf
einer der Platten aufschlagen? Wie weit δy fiel das Elektron durch den Einfluss der Gravitation in dieser Zeit?
 """

import math


voltage = 2
plateDistance = 0.06
electronCharge = 1.60217662e-19
electronMass = 9.10938356e-31
gravity = 9.81

electronField = voltage / plateDistance
force = electronCharge * electronField
acceleration = force / electronMass

dx = plateDistance / 2
dt = math.sqrt(2 * dx / acceleration)
dy = 0.5 * gravity * dt**2

print(dt)
print(dy)
