#set text(font: "Fira Sans")
#set page(height: auto)

// == 1 - Gebräuchliche Winkelmaße

// _Ergänzen Sie die folgende Tabelle, indem Sie die angeführten Winkel in den jeweils fehlenden 
// Winkelmaßen angeben:_

// Auf 3 Nachkommastellen gerundet.

// #align(center)[
//   #table(
//     columns: 5, 
//     align: center,
//     stroke: none,
    
//     [*rad*], [*°*], [*°'"*], [*gon*], [*gon c cc*],
//     [2.173],
//     [124.508],
//     [*(124,30,30.000)*],
//     [138.343],
//     [(138,34,25.926)],
//     [1.953],
//     [111.873],
//     [(111,52,21.720)],
//     [124.303],
//     [*(124,30,30.000)*],
//   )
// ]

// Umwandlung Altgrad in Radiant:
// $ "rad" = pi/180 ("deg" + "min" / 60 + "sec" / 3600) $

// Umwandlung Neugrad in Radiant:
// $ "rad" = pi/200 ("gon" + "c" / 100 + "cc" / 10000) $



// #pagebreak()
// == 2 - Abschätzung: Vertikalwinkelmessung
// _Wie groß muss die Durchbiegung eines Balkens unter Belastung mindestens sein, damit sie mit 
// einem Theodolit durch Messung von Vertikalwinkeln aus 50 m Entfernung aufgedeckt werden 
// kann? Annahmen: Visur annähernd horizontal, Auflösung der Vertikalwinkel: 0.7 mgon._

// Funktionaler Zusammenhang:
// $ h = s tan alpha $ 

// Eingesetzt:
// $
// s &= 50"m" \
// alpha &= 0.7"mgon" \
// h &= 0.55"mm"
// $

// #pagebreak()
// == 3 - Abschätzung: Nivellement aus der Mitte
// _Wie genau muss ein Nivellier mit einer Ziellinienneigung von ω = 10" in der Mitte zwischen den 
// beiden Lattenstandpunkten aufgestellt werden, damit der Einfluss auf den Höhenunterschied unter 
// 0.1 mm bleibt? _

// Überlegung: Bei sehr kleinen Winkeln kann $tan alpha approx alpha$ (mit $alpha$ in Radiant!) angesehen werden.
// Die gemessene Höhe ist daher:
// $ y = alpha x $

// Nun haben Winkel und Abstand jeweils einen Fehler, und produzieren damit einen Höhenfehler:
// $ (y + d y) = (alpha plus d alpha) (x plus.minus d x) $

// Insbesondere ist der Abstandsfehler zu beiden Punkten jeweils gegenläufig, der Winkelfehler jedoch gleich:
// $
// (y_1 + d y_1) = (alpha_1 plus d alpha) (x plus d x) \
// (y_2 + d y_2) = (alpha_2 plus d alpha) (x minus d x) \
// $

// Für die Abstandsberechnung ergibt sich damit ein Gesamtfehler:
// $
// y_1 - y_2 + d y_1 - d y_2 = 
//   alpha_1 x + alpha_1 d x
//   - alpha_2 x + alpha_2 d x +2 d a d x 
// $
// Ersetzt man $alpha x = y$:
// $
//   y_1 - y_2 + d y_1 - d y_2 &= 
//   y_1 + alpha_1 d x
//   - y_2 + alpha_2 d x +2 d a d x  \

//   d y_1 - d y_2 &= 
//   alpha_1 d x + alpha_2 d x +2 d a d x  \

//   d y &= d x (alpha_1  + alpha_2 + 2 d a)
// $

// Ergo: Je höher der gemessene Winkel ist, desto stärker wirkt sich die Verschiebung aus. Geht man von nahezu horizontaler Messung aus mit $a approx 0$, ergibt sich der Zusammenhang:
// $
// d y &= 2  d a d x \
// d x &= (d y) / (2 d a) \
// \
// d y = 0.1 "mm" \
// d a = 10'' \
// underline(d x = 1.03 "m")
// $

// #pagebreak()
// == 4 - Abschätzung: Europabrücke - Erdkrümmungseinfluss
// _Die beiden mittleren Pfeiler der Europabrücke sind jeweils etwa 190 m hoch und am oberen Ende 
// 200 m voneinander entfernt. Die Pfeiler stehen jeweils senkrecht, aufgrund der Erdkrümmung sind 
// sie jedoch nicht parallel. Um wie viel weicht der Abstand an der Pfeilerbasis vom Abstand am 
// oberen Ende ab? _

// "Horizontaler" Abstand $d$ entspricht einem Bogenelement eines Kreises mit Abstand $r$.
// $

// alpha &= d / r =  d_1 / r_1 = d_2 / r_2 \
// d_2 &= d_1 r_2/r_1 \
// \ 
// d_1 &= 200m \
// r_1 &= 6370000m + 190m \
// r_2 &= 6370000m \
// d_2 &= 199.994m \
// underline(d_1 - d_2 &= 0.006m = 6"mm")
// $

// #pagebreak()
// == 5 - Umrechnung zwischen Polarkoordinaten und rechtwinkeligen Koordinaten 
// _Der Richtungswinkel zwischen den Punkten A und B beträgt tAB = 381.720 gon, die Entfernung 
// sAB = 201.344 m; beide Werte sind bereits in ein ebenes Koordinatensystem transformiert worden 
// (Gauß-Krüger). Berechnen Sie die Koordinatendifferenz im mathematisch negativen, 
// rechtwinkeligen Koordinatensystem._

// $
// x &= s sin t \
// y &= s cos t 
// \
// s &= 201.344m \
// t &= 381.720"gon" \
// \
// x &= 193.100"m" \
// y &= -57.023"m" 
// $

// #pagebreak()
// == 6 - Teilkreisorientierung
// _Mit einem Theodolit wurde auf dem Standpunkt P10 die unten angeführten Richtungen (R) zu den Anschlusspunkten P71, P11 und P14 gemessen. Berechnen Sie die Orientierung des Teilkreises. _

// #align(center)[
//   #table(
//     columns: 2,
//     stroke: none,
//     [Koordinatenverzeichnis (GK, M34)], [Richtungsmessung]
//   )
//   #table(
//     columns: 6,
//     align: right,
//     stroke: none,
//     column-gutter: 20pt,
// [*Punktbezeichnung*], [*y [m]*], [*x [m]*], [*von*], [*nach*], [*R [gon]*],
// [P10], [-66182.18], [5215829.07], [],[],[],
// [P11], [-66182.18], [5215834.07], [P10], [P11], [204.7964],
// [P14], [-66136.44], [5215849.28], [P10], [P14], [278.3129],
// [P71], [-66501.20], [5215444.07], [P10], [P71], [48.8534],
//   )
// ]

// Durch Subtraktion der Koordinaten von P10, wodurch der Koordinatenursprung zum Theodoliten verschoben wird, kann die orientierte Richtung $alpha$ der Verbindungsgeraden zu den einzelnen Punkten gemessen werden, und die Differenz $phi$ zur unorientierten Richtung:

// #align(center)[
//   #table(
//     columns: 6,
//     align: right,
//     stroke: none,
//     column-gutter: 20pt,
// [*von*], [*nach*], [*dy [m]*], [*dx [m]*], [*$alpha$ [gon]*], [*$phi$ [gon]*],
// [P10], [P11], [0], [5], [0], [195.204],
// [P10], [P14], [45.74], [20.21], [73.513], [195.200],
// [P10], [P71], [-319.02], [-385.0], [44.051], [195.198],
//   )
// ]

// Der Teilkreis ist nach #underline[195.2 gon] orientiert.

// #pagebreak()
// == 7 - Abschätzung: Auswirkung von Koordinatenfehlern 
// _Die Koordinaten sind im Beispiel (6) auf cm gegeben. Schätzen Sie für jeden der Zielpunkte ab, welche Unsicherheit sich daraus in der berechneten Orientierung ergibt. Sind alle Zielpunkte gleichermaßen für die Berechnung der Orientierung geeignet? Wenn nicht, welche(n) würden Sie bevorzugen, und warum?_

// Funktionaler Zusammenhang:
// $
// f: phi &= alpha - R \
// phi &= arctan(y/x) - R
// $

// Differentiale:
// $
// (delta f) / (delta y) = x / (x^2 + y^2) \
// (delta f) / (delta x) = -y / (x^2 + y^2) \
// $

// Totales Differential:
// $ Delta phi = x / (x^2 + y^2) Delta y -y / (x^2 + y^2) Delta x $

// Die Faktoren vor $Delta y$ und $Delta x$ werden kleiner, je weiter die Punkte entfernt sind. Zur genauen Messung der Teilkreisorientierung sollte daher der am weitesten entfernte Punkt anvisiert werden.

// #align(center)[
//   #table(
//     columns: 5,
//     align: right,
//     stroke: none,
//     column-gutter: 20pt,
// [*von*], [*nach*], [*dy [m]*], [*dx [m]*], [*$Delta phi$ [gon]*],
// [P10], [P11], [0], [5], [6.366], 
// [P10], [P14], [45.74], [20.21], [0.325],
// [P10], [P71], [-319.02], [-385.0], [0.01],
//   )
// ]


// #pagebreak()
// == 8 - Polarpunktberechnung
// _Zusätzlich zu den Beobachtungen aus Beispiel (6) liegen noch die Richtung und Distanz (bereits verebnet, d.h. Wert liegt im GK-System vor) von P10 zu den Neupunkten NA und NB vor. Berechnen Sie die Koordinaten dieser beiden Punkte _

// #align(center)[
//   #table(
//     columns: 4,
//     align: right,
//     stroke: none,
//     column-gutter: 50pt,
//     [*von*], [*nach*], [*R [gon]*], [*d [m]*],
//     [P10], [NA], [87.8787], [172.081], 
//     [P10], [NB], [207.4406], [19.994] 
//   )
// ]

// Polarkoordinaten in rechtwinklige Koordinaten umrechnen, dann auf P10 addieren:
// $
// x = d cos R \
// y = d sin R
// $
// #align(center)[
//   #table(
//     columns: 3,
//     align: right,
//     stroke: none,
//     column-gutter: 50pt,
//     [*Punktbezeichnung*], [*y [m]*], [*x [m]*],
//     [NA], [-66013.21], [5215861.64], 
//     [NB], [-66184.51], [5215809.21],
//   )
// ]


// #pagebreak()
// == 9 - Abschätzung: Trigonometrische Höhenübertragung 
// _Schätzen Sie ab, wie sich der ermittelte Höhenunterschied bei einer Horizontalstrecke von ungefähr 100 m und einem Zenitwinkel von ungefähr 50 gon ändert, wenn sich der gemessene Zenitwinkel geringfügig ändert (z.B. um 2 mgon)._

// Funktionaler Zusammenhang:
// $ f: h = s cot zeta $

// Differential:
// $ (delta f)/(delta zeta) = -s / (sin^2 zeta) $

// Fehlerfortpflanzung:
// $ 
// Delta h &= -s / (sin^2 zeta) Delta zeta \
// $
// Eingesetzt:
// $
// Delta h &= abs(-((100"m"))/(sin^2 (50"gon")) (2"mgon")) \
// Delta h &= 6.28"mm"
// $

// #pagebreak()
// == 10 - Abschätzung: Trigonometrische Höhenübertragung 
// _Schätzen Sie ab, wie sich der ermittelte Höhenunterschied bei einer Horizontalstrecke von ungefähr 100 m ändert, wenn sich zusätzlich zur Änderung des Zenitwinkels (um 2mgon) auch die 
// gemessene Horizontalstrecke geringfügig ändert (z.B. um 5 mm)._

// Funktionaler Zusammenhang:
// $ f: h = s cot zeta $

// Differentiale:
// $
// (delta f)/(delta s) &= cot zeta \
// (delta f)/(delta zeta) &= -s / (sin^2 zeta) \
// $

// Fehlerfortpflanzung:
// $ Delta h = (cot zeta) Delta s -s / (sin^2 zeta) Delta zeta
// $

// Eingesetzt:
// $ Delta h &= abs(cot (50"gon") (5"mm") ) + abs(((100"m")) / (sin^2 (50 "gon")) (2"mgon")) \
// Delta h &= 11.28"mm"
// $


// #pagebreak()
// == 11 - Varianzfortpflanzung: Trigonometrische Höhenübertragung 
// _Welche Standardabweichung hat ein trigonometrisch ermittelter Höhenunterschied über kurze Distanzen ($<=$ 100 m; Achtung: Horizontalstrecke!), wenn die Standardabweichung der Distanzmessung 5 mm beträgt und jene der Zenitwinkelmessung 2 mgon? (Diese Größen werden als untereinander unkorreliert angesehen.)_

// _Geben Sie das Ergebnis zunächst für eine bestimmte Distanz (z.B. 100 m) und einen bestimmten Zenitwinkel (z.B. 50 gon) an. Fertigen Sie dann eine Grafik an, aus der die Standardabweichung in Abhängigkeit vom Zenitwinkel und für verschiedene Entfernungen abgegriffen werden kann._

// Funktionaler Zusammenhang:
// $ f: h = s cot zeta $

// Differentiale:
// $
// (delta f)/(delta s) &= cot zeta \
// (delta f)/(delta zeta) &= -s / (sin^2 zeta) \
// $

// Varianzfortpflanzung:
// $ s_h^2 = (cot zeta)^2 s_s^2 + (-s / (sin^2 zeta))^2 s_zeta^2 $

// Eingesetzt:
// $ s_h^2 &= cot^2 (50"gon") (5"mm")^2 + (-((100"m")) / (sin^2 (50"gon")))^2 (2"mgon")^2 \
// s_h &= 8.03"mm"
// $

// #image("Varianzfortpflanzung.png")

// #pagebreak()
== 12 - Vergleich Abschätzung - Varianzfortpflanzung 
_Vergleichen Sie die Ergebnisse aus Beispiel (10) und Beispiel (11). Stimmen die Ergebnisse
überein? Kommentieren/Erklären Sie warum die Ergebnisse übereinstimmen bzw. nicht
übereinstimmen. _

$
"Beispiel 10:" Delta h &= 11.28 "mm" \
"Beispiel 11:" s_h &= 8.03 "mm"
$

Beispiel 10 ist die Abweichung für den konkreten Fall $Delta zeta = 2 "mgon"$ und $Delta s = 5 "mm"$. \
Beispiel 11 zeigt die Varianz an, wenn diese Werte die Standardabweichung bilden. Allerdings sind in einer Normalverteilung 2/3 der Werte geringer als die Standardabweichung - kleinere Fehler treten häufiger auf, der erwartete Fehler ist daher geringer.

#pagebreak()
== 13 - Varianzfortpflanzung bei Koordinatenumrechung 
_Berechnen Sie die Standardabweichung der Koordinatendifferenzen aus Beispiel (5) unter der
Annahme, dass der Richtungswinkel eine Standardabweichung von 1.5 mgon und die Distanz eine
Standardabweichung von 5 mm hat. (Diese Größen werden als untereinander unkorreliert
angesehen.) _

$
t_"AB" &= 381.720"gon" plus.minus 1.5"mgon" \
s_"AB" &= 201.344"m" plus.minus 5"mm"
$

Funktionaler Zusammenhang:
$
f_1: x &= s sin t \
f_2: y &= s cos t 
$

Totale Differentiale:
$
s_x &= sqrt(((delta f_1)/(delta s))^2 s_s^2 + ((delta f_1)/(delta t))^2 s_t^2) &= sqrt((sin t)^2 s_s^2 + (s cos t)^2 s_t^2) \
s_y &= sqrt(((delta f_2)/(delta s))^2 s_s^2 + ((delta f_2)/(delta t))^2 s_t^2) &= sqrt((cos t)^2 s_s^2 + (-s sin t)^2 s_t^2) \
$

Eingesetzt: 
$
s_x &= sqrt((sin 381.720"gon")^2 (5"mm")^2 + ((201.344"m") (cos 381.720"gon"))^2 (1.5"mgon")^2) &= 4.8 "mm"\
s_y &= sqrt((cos 381.720"gon")^2 (5"mm")^2 + ((-201.344"m") (sin 381.720"gon"))^2 (1.5"mgon")^2) &= 5.0 "mm"\
$

#pagebreak()
== 14 - Teilkreisorientierung
_Wie groß ist die Standardabweichung der berechneten Teilkreisorientierung aus Beispiel (6),
wenn die Standardabweichung der gemessenen Richtungen jeweils 1 mgon beträgt, und jene der
gegebenen Koordinaten jeweils 1 cm (alle Größen untereinander unkorreliert)._

Funktionaler Zusammenhang:
$
f: O &= arctan(y/x) - R
$

Differentiale:
$
(delta f) / (delta y) &= x / (x^2 + y^2) \
(delta f) / (delta x) &= -y / (x^2 + y^2) \
(delta f) / (delta R) &= -1 \
$

Varianzfortpflanzung:
$ 
s_x &= sqrt(2) dot 1 "cm" "(Durch Subtraktion zweier fehlerbehafteter Koordinaten)"\
s_y &= sqrt(2) dot 1 "cm" \
s_R &= 1 "mgon" \
s_O &= sqrt( (x / (x^2 + y^2))^2 s_y^2 + (-y / (x^2 + y^2))^2 s_x^2 + (-1)^2 s_R^2) 

$


#align(center)[
  #table(
    columns: 6,
    align: right,
    stroke: none,
    column-gutter: 20pt,
[*von*], [*nach*], [*dy [m]*], [*dx [m]*], [*R [gon]*], [*$s_O$ [mgon]*],
[P10], [P11], [0], [5], [204.7964], [2.823],
[P10], [P14], [45.74], [20.21], [278.3129], [0.281],
[P10], [P71], [-319.02], [-385.0], [48.8534], [0.032],
  )
]




#pagebreak()
== 15 - Polarpunktberechnung
_Berechnen Sie die Standardabweichung der Koordinaten der Neupunkte NA und NB aus Beispiel
(8) unter der Annahme, dass keine der Eingangsgrößen fix ist. Nehmen Sie z.B. an, die
Standardabweichung der gemessenen Richtungen betrage jeweils 1 mgon, jene der Distanzen
jeweils 5 mm, und jene der gegebenen Koordinaten jeweils 1 cm. _

Funktionaler Zusammenhang:
$
f_1 : y = d sin R + y_"10" \
f_2 : x = d cos R + x_"10" \
$

Differentiale:
#align(center)[
  #grid(columns: 2, gutter: 50pt,
    box($
      (delta f_1) / (delta d) &= sin R \
      (delta f_1) / (delta R) &= d cos R \
      (delta f_1) / (delta y_10) &= 1 \
    $),
    box($
      (delta f_2) / (delta d) &= cos R \
      (delta f_2) / (delta R) &= -d sin R \
      (delta f_2) / (delta x_10) &= 1 \
    $)
  )
]

Varianzfortpflanzung:
$
s_d &= 5 "mm" \
s_R &= 1 "mgon" \
s_x_10 = s_y_10 &= 1 "cm" \
s_y &= sqrt(
  (sin R)^2 s_d^2 +
  (d cos R)^2 s_R^2 + 
  (1)^2 s^2_y_10
) \
s_x &= sqrt(
  (cos R)^2 s_d^2 +
  (-d sin R)^2 s_R^2 + 
  (1)^2 s^2_x_10
) \
$


#align(center)[
  #table(
    columns: 6,
    align: right,
    stroke: none,
    column-gutter: 30pt,
    [*von*], [*nach*], [*R [gon]*], [*d [m]*], [*$s_y$ [mm]*], [*$s_x$ [mm]*],
    [P10], [NA], [87.8787], [172.081],  [11.15], [10.39],
    [P10], [NB], [207.4406], [19.994],  [10.02], [11.17],
  )
]


#pagebreak()
== 16 - Allgemeiner Richtungsschnitt 
_Bei der Messung für einen Polygonzug von KT 130-152 nach KT 136-152 wurden im Anfangs und Endpunkt Richtungen zu den Hochzielen 1-152, 14-152 und einem weiteren Punkt
(Stangensignal) gemessen, dessen Punktbezeichnung und Lage Sie vorerst nicht kennen. Sie wollen ihn aber für die Berechnung der Orientierung bei der späteren Polygonzugsauswertung verwenden. Ermitteln Sie die (Näherungs-) Koordinaten des unbekannten Punktes mittels
allgemeinem Richtungsschnitt, damit Sie ihn am zuständigen Vermessungsamt erheben können! 
_
Koordinatenverzeichnis: GK (M31), auf m gerundet 

#align(center)[
  #table(
    columns: 4,
    align: right,
    stroke: none,
    column-gutter: 50pt,
    [*Pkt.-Nr.*], [*y [m]*], [*x [m]*], [*Anmerkung*],
    [130-152],[-60751],[5207637],[Anfangspunkt Polygonzug],
    [136-152],[-61001],[5208713],[Endpunkt Polygonzug],
    [1-152],[-60176],[5207125],[Kirche Matrei, Knaufv],
    [14-152],[-59252],[5212812],[Nüssingkogel, Stg.-Signal],
    [_Unbekannt_],[],[],[_Unbek. Gipfel, Stg.-Signal_],
  )
]

Messdaten im Anfangs- und Endpunkt des Polygonzugs
#align(center)[
  #table(
    columns: 4,
    align: right,
    stroke: none,
    column-gutter: 50pt,
    [*von*], [*nach*], [*R [g]*], [*Anmerkung*],
    [130-152], [1-152], [144.314], [Kirche Matrei, Knauf],
    [], [14-152], [15.949], [Nüssingkogel, Stg.-Signal], 
    [], [Unbekannt], [42.715], [Unbekannt, Stg.-Signal], 
    [136-152], [1-152], [166.497], [Kirche Matrei, Knauf], 
    [], [14-152], [22.675], [Nüssingkogel, Stg.-Signal], 
    [], [Unbekannt], [60.936], [Unbekannt, Stg.-Signal], 
  )
]

Zunächst wird die Orientierung in den Punkten 130-152 und 136-152 berechnet.
Dazu wird die Koordinatendifferenz aus dem Messpunkt zu den bekannten Hochzielen berechnet, daraus der Richtungswinkel bestimmt und von der gemessenen Richtung abgezogen:

$
  O &= arctan((Delta y) / (Delta x)) - R \
  O_"130-152" &= 2.00"gon" \
  O_"136-152" &= 3.00"gon" \
$

Mittels der Orientierung können nun die unorientierten gemessenen Winkel zum unbekannten Punkt korrigiert werden:

$
  t_"130-152" &= 2.00"gon" + 42.715"gon" &= 44.715"gon" \
  t_"136-152" &= 3.00"gon" + 60.936"gon" &= 63.936"gon" \
$


Und dann mithilfe eines Vorwärtsschnitts (ausgehend von den Punkten 130-152 und 136-152) die Koordinaten des unbekannten Punktes berechnet werden:

$
  d_"12", t_"12" &= "HA2"(p_1, p_2) \
  d_"13" &= d_"12"  sin(t_"23" - t_"12") / sin(t_"23" - t_"13") \
  p_3 &= "HA1"(p_1, d_"13", t_"13")
$

Damit ergeben sich die Koordinaten des unbekannten Punktes:
$
y = -58487"m"\
x = 5210312"m"
$

#image("AllgemeinerRichtungsschnitt.png")


#pagebreak()
== 17 - Nivelliertest
_Je eine Nivellierlatte steht auf den Punkten A und B (Abstand ca. 60m). Das Nivellier wird insgesamt 10 Mal (ISO: 20 Mal) ungefähr in der Mitte zwischen den Latten aufgestellt, und jeweils eine Ablesung auf beiden Latten durchgeführt (Rück- und Vor-Lesung). Der
Höhenunterschied zwischen den Punkten A und B, sowie seine empirische Standardabweichung sind gesucht. _

#align(center)[
  #table(
    columns: 3,
    align: right,
    stroke: none,
    column-gutter: 50pt,
    [*Messung*],[*rück [m]*], [*vor [m]*],
    [1],[1.767],[1.275],
    [2],[1.691],[1.200],
    [3],[1.734],[1.235],
    [4],[1.722],[1.228],
    [5],[1.759],[1.265],
    [6],[1.753],[1.252],
    [7],[1.722],[1.219],
    [8],[1.675],[1.180],
    [9],[1.756],[1.256],
    [10],[1.718],[1.222], 
  )
]

Höhendifferenz:
$
Delta h = h_"vor" - h_"rück"
$

Mittelwert:
$
mu_(Delta h) = 1/n sum_(i=1)^n Delta h_i = -0.4965 "m"
$

Standardabweichung:
$
s_(overline(Delta h)) = sqrt(1/(n-1) sum_(i=1)^n (Delta h_i - mu_(Delta h))^2) = 4.03 "mm"
$


#pagebreak()
== 18 - Gruppenweise Mittelbildung (gewichtetes Mittel) 
_Der Höhenunterschied zwischen den Punkten A und B aus Beispiel (17) soll zunächst für die Gruppen der Beobachtungen 1,2 sowie 3, 4,...,10 getrennt berechnet werden. Aus diesen beiden Mitteln ist das Gesamtmittel zu berechnen und mit dem Ergebnis von vorhin zu vergleichen. Was muss bei der Mittelung der Gruppenergebnisse beachtet werden?_

Bei Differenzbildung einzelner Werte kann stattdessen auch die Differenz aus den Mittelwerten genommen werden.

Bei der Standardabweichung müssen die einzelnen Terme quadriert und dann die Wurzel gezogen werden:

$
s_"Diff" = sqrt(s_"vor"^2 + s_"rück"^2) 
$

#align(center)[
  #table(
    columns: 3,
    stroke: none,
    align: right,
    [*Gruppe*], [*$mu$ [m]*], [*$s$ [mm]*],
    [vor], [1.2332], [29.67],
    [rück], [1.730], [30.27],
    [Differenz], [-0.4965], [42.39],
    [Differenz (Aufgabe 17)], [-0.4965], [4.03]
  )
]

Es fällt auf, dass der Mittelwert der Höhenunterschiede auf beiden Rechenwegen identisch ist, die Standardabweichung sich aber deutlich unterscheidet. Die Ursache dafür ist, dass die Höhenmessung nach vorne und hinten nicht unabhängig, sondern korreliert sind. Grund dafür dürfte die ungenaue Positionierung des Nivelliers zwischen den beiden Punkten sein - dadurch ändert sich zwar nicht die Höhendifferenz (bei einem ausreichend kalibierten Nivellier), jedoch die einzelnen Höhenmessungen pro Latte unterscheiden sich, je nachdem wie nah das Nivellier an der Latte steht.

#image("GruppenweiseMittelbildung.png")