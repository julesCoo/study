import numpy as np

# Dieses Skript wertet Messungen aus, mit dem Ziel einen möglichen Hangrutsch zu überwachen.
#
# Dazu werden mit einem Theodoliten 4 Messpunkte ermittelt und mit historischen Daten verglichen.
# Sofern der Abstand zur früheren Messung zu groß ist, kann von einem Hangrutsch ausgegangen werden.

# Zuerst wird die y/x-Position des Theodoliten ("PKT. 3040") eingelesen:
measuring_position = np.loadtxt("Standpunkt.txt", skiprows=1)

# Mit dem Theodoliten werden die Endpunkte einer Basislatte gemessen, die jeweils in den Messpunkten 1-4
# positioniert wurde. Die Endpunkte der Basislatte wurden anvisiert und der Winkel zwischen diesen gemessen.
# Aufgrund der bekannten Breite der Basislatte lässt sich daraus der Abstand vom Theodoliten zum Messpunkt bestimmen.
# Zur verbesserten Genauigkeit wurde diese Messung jeweils 3x wiederholt. Aus der Datei wird also eine 4x3 Matrix gelesen.

# Winkel wurden in Altgrad gemessen, für die Berechnung müssen sie in Bogenmaß umgewandelt werden.
def gradians_to_radians(gon: float) -> float:
    return gon * np.pi / 200


subtense_angles = np.loadtxt("Basislattenmessungen.txt", skiprows=1)
subtense_angles = gradians_to_radians(subtense_angles)

# Um aus einer Winkelmessung mit der Basislatte die Entfernung zum Messpunkt zu bestimmen, wird diese Formel verwendet.
# Dabei ist b die Breite der Basislatte, und gamma der gemessene Winkel.
def distance_from_angle(gamma: float) -> float:
    b = 2  # Es wurde in diesem Fall eine Basislatte mit einer Breite von 2m verwendet.
    s = (b / 2) / np.tan(gamma / 2)
    return s


# Die Entfernung wird nun für jeden Messwert der Matrix berechnet.
# Anschließend werden aus den Zeilen der Matrix ein Mittelwert berechnet, sodass das Ergebnis ein Array mit 4 Werten ist.
subtense_distances = distance_from_angle(subtense_angles)
subtense_distances = np.mean(subtense_distances, axis=1)

# Anschließend wurden orientierte Richtungen (in gon) zu den Messpunkten gemessen.
# Hier wurde bereits der Mittelwert aus mehreren Messungen gebildet und ist in der Datei abgespeichert.
oriented_angles = np.loadtxt("Gemittelte Orientierte Richtungen.txt", skiprows=1)
oriented_angles = gradians_to_radians(oriented_angles)

# Um die Koordinaten der Messpunkte zu berechnen, wird nun eine Matrix gebildet mit den Spalten:
# | y1, x1, distance, oriented_angle |
# Dabei sind x1 und y1 die Koordinaten des Theodoliten.
# Die Position des Messpunkts lässt sich dann mit der ersten Hauptaufgabe berechnen.
def forward_problem(args):
    # Argument dieser Funktion ist ein Numpy Array, das hier manuell entpackt werden muss..
    y1, x1, s, phi = args
    y2 = y1 + s * np.sin(phi)
    x2 = x1 + s * np.cos(phi)
    return y2, x2


# Natürlich würde man für 4 Messpunkte niemals so einen algorithmischen Aufwand betreiben,
# aber stellen wir uns einfach vor, es wären 40000 Messpunkte, und die Parallisierung würde
# sich lohnen...
num_measurements = 4
forward_matrix = np.stack(
    [
        # Erste Spalte: y-Koordinate.
        # Da diese immer gleich ist, wird sie für alle Zeilen der Matrix wiederholt.
        np.repeat(measuring_position[0], num_measurements),
        # Zweite Spalte: x-Koordinate. Analog zur y-Koordinate.
        np.repeat(measuring_position[1], num_measurements),
        # Dritte Spalte: Entfernung zum Messpunkt.
        subtense_distances,
        # Vierte Spalte: Orientierte Richtung.
        oriented_angles,
    ],
    # Messwerte einer Messung werden in einer Zeile zusammengefasst.
    axis=1,
)

measurement_coordinates = np.apply_along_axis(forward_problem, 1, forward_matrix)
print(measurement_coordinates)
