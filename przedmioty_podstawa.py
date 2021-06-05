

class Przedmiot():
    wartosc = 0
    waga = 0
    nazwa = ""

    def __init__(self, wartosc, masa):
        self.wartosc = wartosc
        self.masa = masa
        self.nazwa = ""

    def zwroc_mase(self):
        return self.masa

    def zwroc_wartosc(self):
        return self.wartosc