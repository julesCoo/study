"""

Dieses Skript wertet die Messwerte einer Frequenzmodulation aus,
und erstellt Diagramme aus diesen Messwerten.

Aus einer Menge von diskreten Winkelwerten x wird eine Funktion y(x) evaluiert
und geplottet.

Anschließend werden "reale" Messwerte für die selben x-Werte genommen und ebenfalls
geplottet.

Die Messwerte sind mit Rauschen behaftet. Dieses Rauschen wird als Differenz der
Messwerte zur Funktion berechnet und ebenfalls geplottet.

"""

import numpy as np
import matplotlib.pyplot as plt


"""

Zunächst werden die Daten geladen.

"""

# Messwerte im CSV-Format. Spalten sind [ID],[Winkel in rad],[y-Wert]
# Die erste Datei enthält einen CSV-Header, die zweite nicht.
# Klassische Kraut- und Rüben-Datenverwaltung...
data = np.loadtxt("winkel_y.txt", delimiter=",", skiprows=1)
data_with_noise = np.loadtxt("data_with_noise.txt", delimiter=",")

"""

Dann werden Hilfsfunktionen definiert.

"""

# Die IDs der Messwerte sind unsortiert in der Datei enthalten.
# Um die xy-Werte zu einer bestimmten ID zu finden, müssen wir
# zwangsläufig die gesamte Matrix durchsuchen, um die passende
# Zeile zu finden.
# Alternativ könnte man die Matrix vorher sortieren, was allerdings
# auch lange dauern könnte. Solange wir vergleichsweise wenige
# IDs anfragen, ist eine vorherige Sortierung aufwändiger.
def xy_from_id(id):
    for row in data:
        if row[0] == id:
            return row[1], row[2]


# Es sollen einige Marker für bestimmte Messpunkte gezeichnet werden.
# Diese Funktion bekommt die Liste der IDs und die Art der Darstellung,
# und zeichnet entsprechend viele Marker in den aktuellen Plot.
def plot_ids(ids, marker):
    for id in ids:
        x, y = xy_from_id(id)
        plt.plot(x, y, marker)


"""

Plot aus Aufgabe a)

"""

# x-Achse zeigt die Winkel in rad, y-Achse zeigt den Funktionswert
xs = data[:, 1]
ys = data[:, 2]

# xy-Kurve als gestrichelte Linie (Farbe aus Vorgabe entnommen).
# Fläche unter der Funktion in semi-transparentem Magenta.
plt.plot(xs, ys, "--", color="#30729f")
plt.fill_between(xs, ys, 0, color="m", alpha=0.2)

# Spezielle IDs laut Vorgabe mit verschiedenen Marker-Symbolen.
plot_ids([345, 219], "g>")
plot_ids([198, 166, 315, 280, 90, 388], "b*")
plot_ids([48, 573, 653, 243, 387, 409], "ro")

# Achsenbeschriftung und Titel
plt.suptitle("Frequenzmodulation", fontweight="bold")
plt.title("mit Δω = 0.5 und Ω=ω/6")
plt.xlabel("Winkel [rad]")
plt.ylabel("Funktion [y = sin(6x . 3cos(x))]")

# Plot speichern und schließen, damit der nächste Plot begonnen werden kann.
plt.savefig("plot_a.png", dpi=400)
plt.close()

"""

Plot aus Aufgabe b)

"""

# x-Achse zeigt die Winkel in rad, y-Achse zeigt den Messwert
xs = data_with_noise[:, 1]
ys = data_with_noise[:, 2]

# xy-Kurve als gestrichelte Linie (Farbe aus Vorgabe entnommen).
# Fläche unter der Funktion in semi-transparentem Magenta.
plt.plot(xs, ys, "--", color="#30729f")
plt.fill_between(xs, ys, 0, color="m", alpha=0.2)

# Achsenbeschriftung und Titel
plt.suptitle("Frequenzmodulation", fontweight="bold")
plt.title("mit Δω = 0.5 und Ω=ω/6 + Rauschen")
plt.xlabel("Winkel [rad]")
plt.ylabel("Funktion [y = sin(6x . 3cos(x))]")

# Plot speichern und schließen, damit der nächste Plot begonnen werden kann.
plt.savefig("plot_b.png", dpi=400)
plt.close()


"""

Plot aus Aufgabe c)

"""

# x-Achse zeigt die Winkel in rad, y-Achse zeigt die Differenz aus Funktionswert und Messwert.
# Es wird davon ausgegangen, dass exakt die selben Messpunkt-IDs in beiden Dateien in der
# selben Reihenfolge auftreten. Andernfalls müsste man erst ein Matching über die ID durchführen.
xs = data_with_noise[:, 1]
ys = data_with_noise[:, 2] - data[:, 2]

# xy-Kurve als geschlossene Linie (Farbe aus Vorgabe entnommen).
# Neu hier ist das Label der Kurve, das anschließend als Legende angezeigt wird.
plt.plot(xs, ys, "-", color="#30729f", label="Rauschen")

# Achsenbeschriftung, Titel und Legende.
plt.suptitle("Rauschen aus Differenzbildung", fontweight="bold")
plt.xlabel("Winkel [rad]")
plt.ylabel("Differenz")
plt.legend()

# Plot speichern und schließen, der Konsistenz wegen.
plt.savefig("plot_c.png", dpi=400)
plt.close()
