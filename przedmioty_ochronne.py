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
    maksymakny_unik = 20
    redukcja = 0
    mnoznik_cen_plyt = ""
    typ = ""

    def __init__(self, czysta_dana):
        super(ElementSzpeju, self).__init__(czysta_dana[-1], czysta_dana[-2])
        self.kamuflaz = "nico"
        self.nazwa = czysta_dana[0]
        self.specjalne = czysta_dana[1]
        self.maksymakny_unik = czysta_dana[2]
        self.redukcja = czysta_dana[3]
        self.maksymalna_pojemnosc = czysta_dana[4]
        self.__obrob_sloty(czysta_dana[5])
        self.mnoznik_cen_plyt = czysta_dana[6]
        magazynki_karabinowe = []
        magazynki_pistoletowe = []
        granaty = []
        apteczka = []

    def __obrob_sloty(self, wejscie):
        wejscie = wejscie.split(",")
        if isinstance(wejscie, list):
            for i in range(0, len(wejscie)):
                wejscie[i] = wejscie[i].strip(" ")
        self.zajmowany_slot = wejscie


