"""
Schreiben Sie ein weiteres Python-Script, in dem Sie das zuvor erstellte Script(funktionen.py) als Python-Modul verwenden.

Beim Import des Moduls soll vorerst noch keine Berechnung erfolgen (ähnlich wiebeim Import von „math“ wo auch noch nichts passiert).
Erst nach dem Import soll zumindest eine der implementierten Funktionen aufgerufen werden.
"""

import funktionen

print(">>>")
print("Aufgabe 1:")

print("Geben Sie einen Winkel in Dezimalgrad ein:")
angle_str = input()
angle_formatted = funktionen.format_angular_input(angle_str)
print(f"Grad: {angle_formatted.degrees}°")
print(f"Min: {angle_formatted.minutes}'")
print(f'Sek: {angle_formatted.seconds:.3f}"')

print("")
print("Aufgabe 2:")
print("Geben Sie die Anzahl der Elemente der Fibonacci Reihe an:")
n = int(input())
print("Output:", funktionen.fibonacci(n))
