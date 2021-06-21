import przedmioty_podstawa as przedmioty_podstawa


class Apteczka(przedmioty_podstawa.Przedmiot):
    specjalne = ""
    premia = 0
    zajmowane_miejsce = ""
    ilosc_ladunkow = 0

    def __init__(self, czysta_dana):
        super(Apteczka, self).__init__(czysta_dana[0], czysta_dana[-2], czysta_dana[-1], )
        self.premia = czysta_dana[1]
        self.specjalne = czysta_dana[2]
        self.zajmowane_miejsce = czysta_dana[3]
        self.ilosc_ladunkow = czysta_dana[4]
