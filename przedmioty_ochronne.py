import przedmioty_podstawa as przedmioty_podstawa
import przedmioty_bron as przedmioty_bron
import przedmioty_inne as przedmioty_inne
import Bot as Bot


class Ubranie(przedmioty_podstawa.Zakladalny):
    kamuflaz = ""

    def __init__(self, czysta_dana):
        super(Ubranie, self).__init__(czysta_dana[-1], czysta_dana[-2], "cialo")
        self.kamuflaz = "nico"

    def wybierz_kamuflaz(self, wejscie):
        if wejscie in ("zimowy", "pustynny", "leśny", "miejski"):
            self.kamuflaz = wejscie
            return True
        else:
            Bot.output("Jeśli chciałeś komuflaż, to powinneś wybrać spośród: \n zimowy, pustynny, leśny, miejski "
                       "\nJeśli chciałeś w innym kolorze, zignoruj tą wiadomość")
            self.kamuflaz = wejscie
            return False


class ElementSzpeju(przedmioty_podstawa.Zakladalny):
    kamuflaz = ""
    magazynki = []
    granaty = []
    apteczka = []
    przedmioty = []
    maksymalna_pojemnosc = 0
    aktualne_oblozenie = 0
    specjalne = []
    maksymakny_unik = 20
    redukcja = 0
    mnoznik_cen_plyt = ""
    typ = ""
    przedmioty_pod_reka = False
    plyta_balistyczna = []

    # handlery do strzelb nie są obsługiwane
    def __init__(self, czysta_dana):
        super(ElementSzpeju, self).__init__(czysta_dana[0], czysta_dana[-2],  czysta_dana[-1], czysta_dana[5])
        self.kamuflaz = "nico"
        self.specjalne = czysta_dana[1]
        self.maksymakny_unik = czysta_dana[2]
        self.redukcja = czysta_dana[3]
        self.maksymalna_pojemnosc = czysta_dana[4]
        self.mnoznik_cen_plyt = czysta_dana[6]
        self.przedmioty = []
        self.aktualne_oblozenie = 0
        self.przedmioty_pod_reka = False
        self.__nastaw_pojemnosc()
        self.__nastaw_mnoznik_plyt()
        if self.mnoznik_cen_plyt:
            self.plyta_balistyczna = PlytyBalistyczne(["brak", "tak", "brak", 0, "", 0, 0])
            # added foo balistic plates

    def kup_i_wloz_plyte_do_kamizelki(self, operator, plyta_jako_rekord):
        plyta = PlytyBalistyczne(plyta_jako_rekord)
        if isinstance(self.mnoznik_cen_plyt, (int, float)):
            if not plyta.rozne_rozmiary:
                Bot.output("nie pasuje!")
                return False
            if plyta.kup(operator):
                self.plyta_balistyczna = plyta
                return True
        else:
            if plyta.specjalne == self.nazwa:
                if plyta.kup(operator):
                    self.plyta_balistyczna = plyta
                    return True
        return False

    def __nastaw_mnoznik_plyt(self):
        if self.mnoznik_cen_plyt == "dedykowana":
            return True
        try:
            i = float(self.maksymalna_pojemnosc)
            self.mnoznik_cen_plyt = i
        except ValueError:
            return False

    def __nastaw_pojemnosc(self):
        if isinstance(self.maksymalna_pojemnosc, str):
            self.przedmioty_pod_reka = True
            mnoznik = 0
            if self.maksymalna_pojemnosc.endswith("a"):
                mnoznik = 1
                self.maksymalna_pojemnosc = int(self.maksymalna_pojemnosc[0:-1])
                self.przedmioty_pod_reka = True
            elif self.maksymalna_pojemnosc.endswith("g"):
                mnoznik = 0.5
                self.maksymalna_pojemnosc = int(self.maksymalna_pojemnosc[0:-1])
                self.przedmioty_pod_reka = True
            elif self.maksymalna_pojemnosc.endswith("12'G"):
                mnoznik = 0.1
                self.maksymalna_pojemnosc = int(self.maksymalna_pojemnosc[0:-4])
                self.przedmioty_pod_reka = True
            elif self.maksymalna_pojemnosc.endswith("k"):
                mnoznik = 0.5
                self.maksymalna_pojemnosc = int(self.maksymalna_pojemnosc[0:-1])
                self.przedmioty_pod_reka = True
            self.maksymalna_pojemnosc = float(self.maksymalna_pojemnosc * mnoznik)

    def wyciagnij_magazynek(self, bron):
        for magazynek in self.przedmioty:
            if isinstance(magazynek, przedmioty_bron.Magazynek):
                if magazynek.amunicja.typ_amunicji == bron.aktualny_magazynek.amunicja.typ_amunicji:
                    if magazynek.stan_nabojow > 0:
                        self.__usun_przedmiot(magazynek)
                        return magazynek
        return False

    def wyciagnij_przedmiot(self, nazwa_przedmiotu):
        for przedmiot in self.przedmioty:
            if przedmiot.nazwa == nazwa_przedmiotu:
                self.__usun_przedmiot(przedmiot)
                return przedmiot

    def schowaj_przedmiot(self, przedmiot):
        oblozenie_przedmiotu = self.sprawdz_oblozenie_przedmiotu(przedmiot)
        if oblozenie_przedmiotu > 0:
            return self.__dodaj_przedmiot(przedmiot)
        return False

    def przyjmij_obrazenia(self, bron, rzut_na_obrazenia):
        if self.mnoznik_cen_plyt:
            if self.plyta_balistyczna.przyjmij_uderzenie(bron):
                return rzut_na_obrazenia - self.redukcja
            return rzut_na_obrazenia

    @staticmethod
    def sprawdz_oblozenie_przedmiotu(przedmiot):
        if isinstance(przedmiot, przedmioty_bron.Magazynek):
            return 0.5
        if isinstance(przedmiot, przedmioty_inne.Apteczka):
            return 1
        if isinstance(przedmiot, przedmioty_bron.Granat):
            return 0.5
        else:
            return 0

    def __usun_przedmiot(self, przedmiot):
        self.przedmioty.remove(przedmiot)
        self.aktualne_oblozenie = self.aktualne_oblozenie - self.sprawdz_oblozenie_przedmiotu(przedmiot)
        return True

    def __dodaj_przedmiot(self, przedmiot):
        self.przedmioty.append(przedmiot)
        self.aktualne_oblozenie += self.sprawdz_oblozenie_przedmiotu(przedmiot)
        return True


class PlytyBalistyczne(przedmioty_podstawa.Przedmiot):  # TODO miękka podkładka still not implemented
    rozne_rozmiary = False
    ochrona = "brak"
    wytrzymalosc = 1
    specjalne = ""

    def __init__(self, czysta_dana):
        super(PlytyBalistyczne, self).__init__(czysta_dana[0], czysta_dana[-2], czysta_dana[-1])
        if czysta_dana[1] == "tak":
            self.rozne_rozmiary = True
        else:
            self.rozne_rozmiary = False
        self.ochrona = czysta_dana[2]
        self.wytrzymalosc = czysta_dana[3]
        self.specjalne = czysta_dana[4]

    def przyjmij_uderzenie(self, bron):
        if self.wytrzymalosc > 0:
            if bron.aktualny_magazynek.amunicja.penetracja > self.ochrona:
                self.wytrzymalosc = 0
                return False
            elif bron.aktualny_magazynek.amunicja.penetracja == self.ochrona:
                self.wytrzymalosc -= 1
                return True
            else:
                return True

