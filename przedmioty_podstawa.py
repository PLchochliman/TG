import constans as constans
import Bot as Bot

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

    def __init__(self, nazwa, masa, wartosc):
        self.wartosc = przerob_stringa_do_int(wartosc, "$")
        self.masa = przerob_stringa_do_float(masa, "kg")
        self.nazwa = nazwa

    def zwroc_mase(self):
        return self.masa

    def zwroc_wartosc(self):
        return self.wartosc

    def zaplac(self, operator):
        if operator.pieniadze >= self.wartosc:
            operator.pieniadze -= self.wartosc
            return True
        Bot.output("nie stać Cię na " + self.nazwa + " brakuje Ci " + str(-1 * operator.pieniadze - self.wartosc) + "$")
        return False

    def zaplac_i_otrzymaj(self, operator):
        if operator.pieniadze >= self.wartosc:
            operator.pieniadze -= self.wartosc
            return self
        Bot.output("nie stać Cię na " + self.nazwa + " brakuje Ci " + str(-1 * operator.pieniadze - self.wartosc) + "$")
        return False


class Zakladalny(Przedmiot):
    zajmowany_slot = ""

    def __init__(self, nazwa, masa, wartosc, slot):
        super(Zakladalny, self).__init__(nazwa, masa, wartosc)
        self.obrob_sloty(slot)

    def obrob_sloty(self, wejscie):
        wejscie = wejscie.split(",")
        if isinstance(wejscie, list):
            for i in range(0, len(wejscie)):
                wejscie[i] = wejscie[i].strip(" ")
        self.zajmowany_slot = wejscie

    def zdejmij(self, operator):
        if isinstance(self.zajmowany_slot, str):
            operator.element_szpeju[constans.miejsce_na_ciele[self.zajmowany_slot]] = ""
            return True
        else:
            for slot in self.zajmowany_slot:
                operator.element_szpeju[constans.miejsce_na_ciele[slot]] = ""
            return True

    def zaloz(self, operator):
        if isinstance(self.zajmowany_slot, str):
            if operator.element_szpeju[constans.miejsce_na_ciele[self.zajmowany_slot]] != "":
                operator.element_szpeju[constans.miejsce_na_ciele[self.zajmowany_slot]] = self
                return True
            return False
        else:
            wolne_sloty = True
            for slot in self.zajmowany_slot:
                if operator.element_szpeju[constans.miejsce_na_ciele[slot]] != "":
                    wolne_sloty = False
            if wolne_sloty:
                for slot in self.zajmowany_slot:
                    operator.element_szpeju[constans.miejsce_na_ciele[slot]] = self
                return True
            return False
