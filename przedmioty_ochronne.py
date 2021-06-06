
import przedmioty_podstawa as przedmioty_podstawa


class Ubranie(przedmioty_podstawa.Przedmiot):
    kolor = ""

    def __init__(self, czysta_dana):
        self.kolor = "nico"


class ElementSzpeju(przedmioty_podstawa.Przedmioty):
    kamuflaz = ""
    magazynki_karabinowe = []
    magazynki_pistoletowe = []
    granaty = []
    apteczka = []
    maksymalna_pojemnosc = 0
    zajmowany_slot = ""
    specjalne = []
    max_unik = 20


    def __init__(self, czysta_dana):
        super(ElementSzpeju, self).__init__(czysta_dana[-1], czysta_dana[-2])
        self.kamuflaz = "nico"
        self.nazwa = czysta_dana[0]
        self.specjalne = czysta_dana[1]
        self.max_unik = czysta_dana[2]

        self.maksymalna_pojemnosc = czysta_dana[4]
        self.zajmowany_slot = czysta_dana[6]
        magazynki_karabinowe = []
        magazynki_pistoletowe = []
        granaty = []
        apteczka = []