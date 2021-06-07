

def przerob_stringa_do_int(zmienna, zmiana):
    if isinstance(zmienna, str):
        zmienna = zmienna.replace(zmiana, "")
        zmienna = zmienna.replace(" ", "")
        zmienna = zmienna.replace(",", ".")
    zmienna = float(zmienna)
    return int(zmienna)


def przerob_stringa_do_float(zmienna, zmiana):
    if isinstance(zmienna, str):
        zmienna = zmienna.replace(zmiana, "")
        zmienna = zmienna.replace(" ", "")
        zmienna = zmienna.replace(",", ".")
    return float(zmienna)


class Przedmiot():
    wartosc = 0
    waga = 0
    nazwa = ""

    def __init__(self, wartosc, masa):
        self.wartosc = przerob_stringa_do_int(wartosc, "$")
        self.masa = przerob_stringa_do_float(masa, "kg")
        self.nazwa = ""

    def zwroc_mase(self):
        return self.masa

    def zwroc_wartosc(self):
        return self.wartosc
