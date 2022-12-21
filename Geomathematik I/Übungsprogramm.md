# Deckblatt

Technischer Bericht, LV, Semester, Name, MatrikelNr, Name des Übungsprogramms

# Inhaltsverzeichnis

# Aufgabenstellung

Eigene Worte

# Durchführung

Alle Formeln erklären.
Formeln durchnummerieren.
Abbildung referenzieren, Subtext.

# Ergebnisse

Interpretation

Abgabe in Bügelmappe!

# Selbstständigkeitserklärung

# 1. Übungsprogramm: Geomathematik / Geomathematik I, WS2022/23

## Orthogonale Transformationen - Plattentektonik

### Aufgabe a

#### Bestimmung der 3D-Koordinaten.

Die Positionen der Messstationen sind gegeben durch:

|                   | geo. Breite | geo. Länge |
| ----------------- | ----------- | ---------- |
| Fort Davis, TX    | 30°38'      | -103°57'   |
| Mammoth Lakes, CA | 37°38'      | -118°56'   |
| Columbus, OH      | 40°         | -83°       |

Diese Angaben beziehen sich auf geographische Polarkoordinaten, also Koordinaten auf der Erdoberfläche. Zu beachten ist, dass die Angaben in Neugrad und Neuminuten angegeben sind.

Zunächst müssen die Angaben in Polarkoordinaten ($\phi$ für geografische Breite und $\lambda$ für geografische Länge) umgerechnet werden. Dazu werden die angegebenen Winkel in Radians umgerechnet und entsprechend zugewiesen.

Siehe die Funktion `from_gon` im Anhang.

|                   | $\phi$  | $\lambda$ |
| ----------------- | ------- | --------- |
| Fort Davis, TX    | 0.47721 | -1.62687  |
| Mammoth Lakes, CA | 0.58716 | -1.86234  |
| Columbus, OH      | 0.62832 | -1.30376  |

Aus diesen Polarkoordinaten lassen sich nun 3D-Koordinaten berechnen. Dabei wird die Vorschrift verwendet:

$$\begin{aligned}
 x &= cos(\phi) cos(\lambda) \\
 y &= cos(\phi) sin(\lambda) \\
 z &= sin(\phi)
\end{aligned}$$

