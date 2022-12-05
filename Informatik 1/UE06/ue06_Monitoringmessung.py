"""

Dieses Skript wertet Messungen aus, mit dem Ziel einen möglichen Hangrutsch zu überwachen.

Dazu werden mit einem Theodoliten 4 Messpunkte ermittelt und mit historischen Daten verglichen.
Sofern der Abstand zur früheren Messung zu groß ist, kann von einem Hangrutsch ausgegangen werden.

"""

import numpy as np

"""

Wir beginnen mit der Definition einiger Funktionen:

"""


# Winkel wurden in Altgrad gemessen, für die Berechnung müssen sie in Bogenmaß umgewandelt werden.
def gradians_to_radians(gon):
    return gon * np.pi / 200


# Um aus einer Winkelmessung mit der Basislatte die Entfernung zum Messpunkt zu bestimmen, wird diese Formel verwendet.
# Dabei ist b die Breite der Basislatte, und gamma der gemessene Winkel.
def subtense_distance_from_angle(gamma):
    b = 2  # Es wurde in diesem Fall eine Basislatte mit einer Breite von 2m verwendet.
    s = (b / 2) / np.tan(gamma / 2)
    return s


"""

Anschließend werden die Messwerte aus .txt Dateien (im TSV-Format) eingelesen und ggf. transformiert.

"""

# Die y/x-Position des Theodoliten ("PKT. 3040"), von dem die Messung ausgeht.
# Eine einzelne Position mit 2 Werten, also eine 1x2 Matrix.
theodolite_position = np.loadtxt("Standpunkt.txt", skiprows=1)

# Mit dem Theodoliten werden die Endpunkte einer Basislatte gemessen, die jeweils in den Messpunkten 1-4
# positioniert wurde. Die Endpunkte der Basislatte wurden anvisiert und der Winkel zwischen diesen gemessen.
# Aufgrund der bekannten Breite der Basislatte lässt sich daraus der Abstand vom Theodoliten zum Messpunkt bestimmen.
# Zur verbesserten Genauigkeit wurde diese Messung jeweils 3x wiederholt. Aus der Datei wird also eine 4x3 Matrix gelesen.
subtense_angles = np.loadtxt("Basislattenmessungen.txt", skiprows=1)
# Es wird der Mittelwert der Winkelmessungen genommen, die Matrix ist nun also 4x1.
subtense_angles = np.mean(subtense_angles, axis=1)
# Die Winkel werden in Bogenmaß umgewandelt für die weitere Berechnung.
subtense_angles = gradians_to_radians(subtense_angles)

# Außerdem wurden orientierte Richtungen (in gon) zu den Messpunkten gemessen.
# Hier wurde bereits der Mittelwert aus mehreren Messungen gebildet und ist in der Datei abgespeichert.
# Die Matrix ist also 4x1.
oriented_angles = np.loadtxt("Gemittelte Orientierte Richtungen.txt", skiprows=1)
# Die Winkel werden in Bogenmaß umgewandelt für die weitere Berechnung.
oriented_angles = gradians_to_radians(oriented_angles)

# Zum Vergleich werden die in 2019 gemessenen Positionen der Messpunkte herangezogen.
# Das Format dieser Datei enthält 2 Zeilen Header, und es werden abwechselnd
# Y und X-Koordinaten der 4 Messpunkte in eine Zeile geschrieben.
# Das Ergebnis hier ist also eine 2x4 Matrix.
coordinates_2019 = np.loadtxt("Monitoringmessung November 2019.txt", skiprows=2)
# Damit Werte für einen einzelnen Messpunkt in einer Zeile stehen (y/x), wird die Matrix transponiert.
# Das Ergebnis ist also eine 4x2 Matrix.
coordinates_2019 = coordinates_2019.transpose()

"""

Nun kann aus den eingelesenen Werten die Position der Messpunkte bestimmt werden.

"""

# Natürlich würde man für 4 Messpunkte niemals so einen algorithmischen Aufwand betreiben,
# aber stellen wir uns einfach vor, es wären Millionen Messpunkte, und die Parallisierung
# über Numpy würde sich lohnen...
num_measurements = 4

# Aus den Winkel-Messungen an der Basislatte lässt sich die Distanz vom Geodoliten zum Messpunkt berechnen.
# Das Ergebnis ist eine 4x1 Matrix.
subtense_distances = subtense_distance_from_angle(subtense_angles)

# Es ist nun alles bekannt, was für die erste Hauptaufgabe benötigt wird:
y = theodolite_position[0]
x = theodolite_position[1]
s = subtense_distances
phi = oriented_angles

# Die y/x-Positionen der Messpunkte können Vektor-weise berechnet werden,
# und dann in eine 4x2 Matrix zusammengefasst werden.
coordinates_2022_y = y + s * np.sin(phi)
coordinates_2022_x = x + s * np.cos(phi)
coordinates_2022 = np.stack([coordinates_2022_y, coordinates_2022_x], axis=1)

# Jetzt lässt sich die Abweichung der neuen Messung zur historischen Messung berechnen.
coordinates_delta = coordinates_2022 - coordinates_2019

"""

Es folgt die Ausgabe der Ergebnisse.

"""

print(">>>")
print("Monitoringmessung")

print("-------------------")
print(f"Standpunkt X[m] = {theodolite_position[1]:.5f}")
print(f"Standpunkt Y[m] = {theodolite_position[0]:.5f}")

print("---")
print("MP-Punkte 2019:")
for i in range(num_measurements):
    print(f"MP{i+1} X[m] = {coordinates_2019[i, 1]:.5f}")
    print(f"MP{i+1} Y[m] = {coordinates_2019[i, 0]:.5f}")
    print("")

print("---")
print("MP-Punkte 2022:")
for i in range(num_measurements):
    print(f"MP{i+1} X[m] = {coordinates_2022[i, 1]:.5f}")
    print(f"MP{i+1} Y[m] = {coordinates_2022[i, 0]:.5f}")
    print("")

print("---")
print("Vergleich:")
for i in range(num_measurements):
    print(f"MP{i+1} dX[mm] = {coordinates_delta[i, 1]*1000:.5f}")
    print(f"MP{i+1} dY[mm] = {coordinates_delta[i, 0]*1000:.5f}")
    print("")
