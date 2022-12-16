# -- coding: utf-8 --
"""
Created on Fri Dec  9 11:09:34 2022

@author: Daniel & Alexander
"""

# Erstellt Klasse Student


class Student:

    # Legt Instanzattribute fest
    matrNr = -1
    vorname = ""
    nachname = ""
    gebDatum = []
    email = ""
    telNr = ""

    # Private Funktion zum Eintragen von Werten
    def ___daten_eintragen(self, matrNr, vorname, nachname, gebDatum, telNr):

        # Schreibt die übergebenen Werte an die Instanzattribute
        self.matrNr = matrNr
        self.vorname = vorname
        self.nachname = nachname
        self.gebDatum = gebDatum
        self.email = f"{vorname}.{nachname}@student.tugraz.at".lower()
        self.telNr = telNr

    # Funktion zum Übertragen von Werten
    def daten_uebergeben(self, matrNr, vorname, nachname, gebDatum, telNr):

        # Überprüft ob übergebene Werte vom richtigen Typ sind und gibt wenn notwendig eine Fehlermeldung aus
        if not isinstance(matrNr, int):
            print("matrNr muss vom Typ int sein!")
            return
        if not isinstance(vorname, str):
            print("vorname muss vom Typ int sein!")
            return
        if not isinstance(nachname, str):
            print("nachname muss vom Typ int sein!")
            return
        if not isinstance(gebDatum, list):
            print("gebDatum muss vom Typ int sein!")
            return
        if not isinstance(telNr, str):
            print("telNr muss vom Typ int sein!")
            return
        # Werte werden mittels vorher definierten Funktion Eingetragen
        else:
            self.___daten_eintragen(matrNr, vorname, nachname, gebDatum, telNr)

    # Funktion um Werte auszugeben
    def daten_ausgeben(self):
        # Gibt Werte der Reihe nach aus
        print("_____________")
        print(self.matrNr)
        print(self.vorname)
        print(self.nachname)
        print(self.gebDatum)
        print(self.email)
        print(self.telNr)
        print("_____________")


print("----------------- Aufgabe 1 -----------------")

# Alexander Arzberger wird als Student angelegt
AlexanderArzberger = Student()
AlexanderArzberger.daten_uebergeben(
    matrNr=11814630,
    vorname="Alexander",
    nachname="Arzberger",
    gebDatum=[23, 11, 2002],
    telNr="06805000433",
)

# Die Werte von Alexander Arzberger werden ausgegeben
AlexanderArzberger.daten_ausgeben()

# Michaek Baum wird als Student angelegt

MichaelBaum = Student()
MichaelBaum.daten_uebergeben(
    matrNr=18742069,
    vorname="Michael",
    nachname="Baum",
    gebDatum=[21, 1, 1999],
    telNr="+43 133",
)

print("----------------- Aufgabe 2 -----------------")

# Erstellt Klasse AlleStudierende


class AlleStudierende:
    # Erstellt Klassenattribut szudent als leere Liste für Objekte der Klasse Student
    student = []

    # Funktion,die das Klassenattribut student um ein Element erweitert und daraufhin Werte übergibt
    def NeuerStudent(self, matrNr, vorname, nachname, gebDatum, telNr):
        student = Student()
        self.student.append(student)
        student.daten_uebergeben(matrNr, vorname, nachname, gebDatum, telNr)

    # Funktion die alle Elemente der Liste student ausgibt
    def AlleStudentendatenAusgeben(self):
        # Für jedes Objekt in der Liste Student wird dieses ausgegeben
        for objects in self.student:
            objects.daten_ausgeben()

    # Funktion zum Löschen eines Elemets aus der Liste student
    def StudentLoeschen(self, matrNr):
        # Jedes Element der Liste student wird nach der übergebenen matrNr durchsucht und gegebenenfalls gelöscht
        for student in self.student:
            if student.matrNr == matrNr:
                self.student.remove(student)
                print(f"Student {student.vorname}{student.nachname} gelöscht!")


AlleStudierende = AlleStudierende()

# Vorherige Daten werden übertragen
AlleStudierende.NeuerStudent(
    matrNr=11814630,
    vorname="Alexander",
    nachname="Arzberger",
    gebDatum=[23, 11, 2002],
    telNr="06805000433",
)

AlleStudierende.NeuerStudent(
    matrNr=18742069,
    vorname="Michael",
    nachname="Baum",
    gebDatum=[21, 1, 1999],
    telNr="+43 133",
)

# Neuer Eintrag
AlleStudierende.NeuerStudent(
    matrNr=23421424,
    vorname="Maria",
    nachname="Musterfrau",
    gebDatum=[11, 3, 1983],
    telNr="+43 122",
)

# Alle Daten werden ausgegeben
AlleStudierende.AlleStudentendatenAusgeben()

# Student wird Gelöscht
AlleStudierende.StudentLoeschen(18742069)

# Alle Daten werden ausgegeben
AlleStudierende.AlleStudentendatenAusgeben()
