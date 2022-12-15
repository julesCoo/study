"""

Aufgabe 1 

"""


class Student:
    matrNr: int = -1
    vorname: str = ""
    nachname: str = ""
    gebDatum: list[int] = []
    email: str = ""
    telNr: str = ""

    def __init__(self):
        # Leerer Konstruktor kann auch weggelassen werden.
        pass

    # Achtung: Ganz schlechter Stil!
    # Daten sollten immer direkt dem Konstruktor übergeben werden, um
    # zu vermeiden dass ungültige Objekte erstellt und im Programm verschwinden
    # können.
    # Für die Übung okay.
    def Datenuebergeben(self, matrNr, vorname, nachname, gebDatum, telNr):
        if not isinstance(matrNr, int):
            print("matrNr muss vom Typ int sein!")
            return
        if not isinstance(vorname, str):
            print("vorname muss vom Typ string sein!")
            return
        if not isinstance(nachname, str):
            print("nachname muss vom Typ string sein!")
            return
        if not isinstance(gebDatum, list):
            print("gebDatum muss vom Typ list sein!")
            return
        if not isinstance(telNr, str):
            print("telNr muss vom Typ string sein!")
            return

        self.__DatenEintragen(matrNr, vorname, nachname, gebDatum, telNr)

    def __DatenEintragen(self, matrNr, vorname, nachname, gebDatum, telNr):
        self.matrNr = matrNr
        self.vorname = vorname
        self.nachname = nachname
        self.gebDatum = gebDatum
        self.telNr = telNr

        self.email = f"{vorname}.{nachname}@student.tugraz.at".lower()

    def DatenAusgeben(self):
        print("________________________________")
        print(self.matrNr)
        print(self.vorname)
        print(self.nachname)
        print(self.gebDatum)
        print(self.email)
        print(self.telNr)
        print("________________________________")
        pass


HaydenStein = Student()
HaydenStein.Datenuebergeben(
    matrNr=12217432,
    vorname="Hayden",
    nachname="Stein",
    gebDatum=[2000, 11, 21],
    telNr="+436608387412",
)

IsabellaGarza = Student()
IsabellaGarza.Datenuebergeben(
    matrNr=12212764,
    vorname="Isabelle",
    nachname="Garza",
    gebDatum=[2000, 1, 1],
    telNr="+436607654321",
)

HaydenStein.DatenAusgeben()
IsabellaGarza.DatenAusgeben()

"""

Aufgabe 2

"""


class AlleStudierende:
    # FIXME: sollte studierende heißen, ist ja eine Liste
    student: list[Student] = []

    def NeuerStudent(self, matrNr, vorname, nachname, gebDatum, telNr):
        student = Student()
        student.Datenuebergeben(matrNr, vorname, nachname, gebDatum, telNr)

        # Aufpassen, dass keine uninitialisierten Objekte in unserer Liste landen.
        # Aus diesem Grund wäre ein Exception besser als eine Fehlermeldung via print().
        if student.matrNr != -1:
            self.student.append(student)

    def AlleStudentendatenAusgeben(self):
        for student in self.student:
            student.DatenAusgeben()

    def StudentLoeschen(self, matrNr):
        for student in self.student:
            if student.matrNr == matrNr:
                self.student.remove(student)
                print(f"Student {student.vorname} {student.nachname} gelöscht!")
                return

        print("Student nicht gefunden!")


StudierendenRegister = AlleStudierende()

StudierendenRegister.NeuerStudent(
    matrNr=12216327,
    vorname="Carlos",
    nachname="Underwood",
    gebDatum=[2001, 2, 24],
    telNr="+436601234567",
)

StudierendenRegister.NeuerStudent(
    matrNr=12215783,
    vorname="Carrie",
    nachname="Hoffman",
    gebDatum=[2000, 6, 18],
    telNr="+436607654321",
)


StudierendenRegister.AlleStudentendatenAusgeben()
StudierendenRegister.StudentLoeschen(matrNr=12215783)

StudierendenRegister.AlleStudentendatenAusgeben()
