#set text(font: "Fira Sans")
#set page(height: auto)

== 24 - Streckenreduktion (atmosphärische Reduktion)
_Sie messen mit einem elektronischen Distanzmesser (Leica DI1000) eine schräge Strecke von s = 978.125 m und möchten diese wegen des Einflusses der Atmosphäre korrigieren. Dazu messen Sie die Temperatur (t = 25°C) und den Luftdruck (p = 870 hPa) und reduzieren laut der angegebenen Korrekturformel._

_Wie lautet die meterologisch reduzierte Strecke? Mit welcher Genauigkeit (Standardabweichung) erhalten Sie die meteorologisch reduzierte Strecke, wenn Sie die Temperaturmessung mit ±2°C und die Luftdruckmessung mit ±5 hPa durchführen können?_

_Meteorologische Reduktion für den Leica DI 1000_

$
Delta s &= (282.2 - (0.2908 p)/(1 + 0.00366 t)) s dot.op 10^(-6) \
s_"red." &= s + Delta s \
\
Delta s &"- Korrektur in [m]" \
p &"- gemessener Luftdruck in [hPa]" \
t &"- gemessene Temperatur in [°C]" \
s &"- gemessene (angezeigte) unreduzierte Strecke in [m]" \
s_"red." &"- meteorologisch reduzierte Strecke in [m]" \
$

Durch Einsetzen:
$
Delta s &= (282.2 - (0.2908 dot.op 870)/(1 + 0.00366 dot.op 25)) dot.op 10^(-6) &= 0.049 m \
s_"red." &= 978.125 + 0.049 &= 978.174 m
$

Für die Varianzfortpflanzung:
$
(delta s_"red.")/(delta t) &= (1.06433 dot.op 10^(-9) p s)/(0.00366 t + 1)^2 \
(delta s_"red.")/(delta p) &= -(2.908 dot.op 10^(-7) s)/(0.00366 t + 1) \
\
sigma_t &= 2 "°C" \
sigma_p &= 5 "hPA" \
sigma_s_"red." &= sqrt(
  ((delta s_"red.")/(delta t))^2 sigma_t^2 +
  ((delta s_"red.")/(delta p))^2 sigma_p^2
) = 0.002 "m"
$


#pagebreak()
== 25 - Streckenreduktion (geometrische Reduktion)
_Für die näherungsweise geometrische Reduktion von gemessenen Horizontalstrecken $s_"hor"$ auf die Sehne am Ellipsoid $s_"ell"$ gilt die angegebene Reduktionsformel. Wie genau müssen Sie die mittlere Höhe des Projektgebietes Hm kennen, damit der Einfluss der geometrischen Reduktion für eine Strecke von s = 100 m (fehlerfrei) unter 0.5 mm bleibt (Erdradius R = 6379 km, fehlerfrei)?_

_Geometrische Streckenreduktion (Vereinfachung für kurze Horizontalstrecken)_

$
s_"ell" = (1 - H_m / R) s_"hor" \
\
s_"ell" &"- Ellipsoidsehne" \
H_m &"- mittlere Projekthöhe" \
R &"- Erdradius" \
s_"hor" &"- gemessene Horizontalstrecke" \
$

Die Varianzfortpflanzung ergibt:
$
e &= (1 - H/R) s "(Vereinfachte Formel)" \ 
(delta e)/(delta H) &= -s / R \
\

sigma_e &= sqrt( (-s / R)^2 sigma^2_H ) &= 0.0005 "m" \
sigma_H &= R / s sigma_e &= 31.895 "m"
$


#pagebreak()
== 26 - Streckenreduktion (Gauß-Krüger-Reduktion) 
_Fertigen Sie eine Grafik an, welche den Reduktionsbetrag der GK-Reduktion in Abhängigkeit von der mittleren y-Koordinate von $y_m$ = 0 km bis $y_m$ = 150 km in Schritten von 30 km für eine Strecke (Ellipsoidbogen) von $s_"ell"$ = 100 m ausweist. Ab wann wird der Reduktionsbetrag für diese Strecke größer als 10 mm?_

_Gauß-Krüger Reduktion (Vereinfachung für kurze Strecken)_
$
s_"GK" = (1 + (y^2_m) / (2 R^2)) s_"ell" \
\
s_"GK" &"- Gauß-Krüger-Strecke" \
y_m &"- mittlere y-Koordinate" \
R &"- Erdradius" \
s_"ell" &"- Ellipsoidsehne (= Sehne bei kurzen Strecken)" \
$

#image("26.png")

$
s_"ell" &= 100 "m" \
R &= 6379 "km" \
Delta s &= s_"GK" - s_"ell" = (y^2_m) / (2 R^2) s_"ell" &= 10 "mm" \
y_m &= sqrt((2 Delta s R^2) / s_"ell") &= 90.213 "km" \
$


#pagebreak()
== 27 - Exzenterberechnung (Direkter Anschluss)
_Für die Bestimmung der Koordinaten eines südwestlich vom Zentrum gelegenen exzentrischen Standpunktes Ex wurden mit einer Totalstation Beobachtungen zum Zentrum Z (Richtung R und Strecke dGK) und zu zwei Fernzielen F1 und F2 (nur Richtungen R) durchgeführt („Direkter Anschluss“), siehe Messprotokoll (die Strecke dGK vom Exzenter zum Zentrum ist bereits in die Gauß-Krüger-Ebene reduziert)._

_a) Fertigen Sie eine lagerichtige Skizze der Situation an!_
_b) Berechnen Sie die Koordinaten des exzentrischen Standpunktes Ex!_
_c) Sind die Beobachtungen aus dem Messprotokoll für eine kontrollierte Bestimmung des Exzentrums ausreichend? Wenn ja, begründen Sie warum, wenn nein, weisen Sie auf kritische Elemente hin und machen Sie Vorschläge zur Verbesserung!_

_*Messprotokoll:*_
#align(center)[
  #table(
    columns: 4,
    align: center,
    stroke: none,
    [*Standpunkt*], [*Zielpunkt*],  [*R [g]*],  [*dGK [m]*],
    [Ex],           [Z],            [13.3825],  [27.763],
    [],             [F1],           [244.0851], [],
    [],             [F2],           [349.6782], [],
  )
]

_*Koordinatenverzeichnis: System Gauß-Krüger, M31*_
#align(center)[
  #table(
    columns: 4,
    align: center,
    stroke: none,
    [*Pkt.-Nr.*], [*y [m]*], [*x [m]*], [*Anmerkung*],
    [Z],          [31580.610], [5223806.430], [Zentrum],
    [F1],         [22159.230], [5220985.460], [Fernziel],
    [F2],         [30237.940], [5230284.730], [Fernziel],
  )
]


Es handelt sich um einen Rückwärtsschnitt mit den beiden Randpunkten F2 und F1, und dem zentralen Punkt Z.

Von Ex aus werden die Winkel zwischen F1 und Z, sowie zwischen Z und F2 gemessen:

$
alpha &= t_"FF-Z" &= 63.7043 "gon" \
beta &= t_"Z-F1" &= 230.7026 "gon" \
$

#figure(
  image("27a.png"), 
  caption: [Messaufbau im lokalen System der Totalstation.]
)

Da die Koordinaten der Punkte bekannt sind, lassen sich die Strecken zwischen ihnen berechnen.

$
d_"F1_Z" &= 9834.647 "m" \
d_"F2_Z" &= 6615.976 "m" \
$

#figure(
  image("27b.png"), 
  caption: [Lage der drei bekannten Punkte im Gauß-Krüger-System]
)

Mithilfe der Winkel und Strecken lässt sich ein Rückwärtsschnitt rechnen. Daraus ergeben sich die Koordinaten des Standpunktes Ex. 

$
y_"Ex" &= 31569.048 "m" \
x_"Ex" &= 5223795.164 "m"
$

#figure(
  image("27c.png"), 
  caption: [Vergrößerter Ausschnitt der Lage im Gauß-Krüger-System]
)

Für eine bessere Messung sollten die Winkel $alpha$ und $beta$ möglichst gleich groß sein, eine bessere Position des Exzenters wäre also weiter links.

Für amtliche Messung ist dieses Verfahren aber ohnehin nicht zulässig für eine genaue Punktbestimmung des Exzenters. 