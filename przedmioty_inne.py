import przedmioty_podstawa as przedmioty_podstawa


class Apteczka(przedmioty_podstawa.Przedmiot):
    specjalne = ""
    premia = 0
    zajmowane_miejsce = ""
    ilosc_ladunkow = 0

    def __init__(self, czysta_dana):
        super(Apteczka, self).__init__(czysta_dana[0], czysta_dana[-2], czysta_dana[-1])
        self.premia = czysta_dana[1]
        self.specjalne = czysta_dana[2]
        self.zajmowane_miejsce = czysta_dana[3]
        self.ilosc_ladunkow = czysta_dana[4]

    def wylecz(self, operator, cel, umiejetnasc="dyscyplina naukowa Medycyna"):
        wynik = operator.rzut_na_umiejetnasc(umiejetnasc)
        self.ilosc_ladunkow -= 1
        if umiejetnasc in ("survival"):
            wynik = wynik - 5
        rana_do_efektu = {"drasniecie": 5,
                          "lekka rana": 5,
                          "rana konczyny": 5,
                          "powazna rana": 15,
                          "krytyczna rana": 15
                          }
        wynik = self.__ktora_rana_zaleczona(wynik)
        efekt = rana_do_efektu[wynik]
        if wynik:
            for propozycja in ("krytyczna rana", "powazna rana", "lekka rana", "rana konczyny", "drasniecie"):
                if rana_do_efektu[propozycja] >= efekt:
                    if cel.wylecz(wynik):
                        return True
        return False

    @staticmethod
    def __ktora_rana_zaleczona(wynik):
        if wynik >= 20:
            return "krytyczna rana"
        if wynik >= 15:
            return "powazna rana"
        if wynik >= 10:
            return "lekka rana", "rana konczyny"
        if wynik >= 5:
            return "drasniecie"
        return False
