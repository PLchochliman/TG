import constans as constans

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


class Zakladalny(Przedmiot):
    zajmowany_slot = ""

    def __init__(self, wartosc, masa, slot):
        super(Zakladalny, self).__init__(wartosc, masa)
        self.obrob_sloty(slot)

    def obrob_sloty(self, wejscie):
        wejscie = wejscie.split(",")
        if isinstance(wejscie, list):
            for i in range(0, len(wejscie)):
                wejscie[i] = wejscie[i].strip(" ")
        self.zajmowany_slot = wejscie

    def zdejmij(self, operator):
        if isinstance(self.zajmowany_slot, str):
            operator.miejsce_na_ciele[constans.miejsce_na_ciele(self.zajmowany_slot)] = ""
            return True
        else:
            for slot in self.zajmowany_slot:
                operator.miejsce_na_ciele[constans.miejsce_na_ciele(slot)] = ""
            return True

    def zaloz(self, operator):
        if isinstance(self.zajmowany_slot, str):
            if operator.miejsce_na_ciele[constans.miejsce_na_ciele[self.zajmowany_slot]] != "":
                operator.miejsce_na_ciele[constans.miejsce_na_ciele[self.zajmowany_slot]] = self
                return True
            return False
        else:
            wolne_sloty = True
            for slot in self.zajmowany_slot:
                if operator.miejsce_na_ciele[constans.miejsce_na_ciele[slot]] != "":
                    wolne_sloty = False
            if wolne_sloty:
                for slot in self.zajmowany_slot:
                    operator.miejsce_na_ciele[constans.miejsce_na_ciele[slot]] = self
                return True
            return False
