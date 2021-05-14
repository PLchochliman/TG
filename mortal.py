"""
it's all about alive objects, which could be destroyed (eg hero, enemy, elephant)
"""
import Bot
import constans


class IstotaZywa: #pełne pokrycie
    sila, zrecznasc, intelekt = 0, 0, 0,
    mod_sila, mod_zrecznosc, mod_intelekt = 0, 0, 0,
    status = True
    rany = []
    redukcja_obrazen, typ_ochrony = 0, 0
    imie = ""
    typ_budowy = []
    mozliwosc_aktywacji = []
    bazowy_unik = 10
    unik = 10
    punktyWytrwalosci, przeznaczenie = 0, 0,
    udzwig = 0
    umiejetnosci = []
    jezyki = []
    planowane_dzialania = []
    oslona = 0
    w_ruchu = 0

    def __init__(self, sila, zrecznasc, intelekt, imie="Bot", unik=10, redukcjaObrazen=0, typOchrony=0):
        self.sila = sila
        self.zrecznasc = zrecznasc
        self.intelekt = intelekt
        self.mod_sila = constans.mod(sila)
        self.modZrecznasc = constans.mod(zrecznasc)
        self.mod_intelekt = constans.mod(intelekt)
        self.imie = imie
        self.typ_budowy = constans.TypBudowy[self.mod_sila]
        self.mozliwosc_aktywacji = constans.TypyAktywacji[self.modZrecznasc]
        self.bazowy_unik = unik + self.modZrecznasc + self.mod_intelekt
        self.unik = self.bazowy_unik         #na razie jest bez sensu, ale w późniejszych rozrachunkach bedzie potrzebne
        self.punktyWytrwalosci = self.intelekt * 2
        self.przeznaczenie = self.mod_intelekt + 1
        self.typ_ochrony = typOchrony
        self.udzwig = self.sila * 5
        self.rany = [0, 0, 0, 0, [0, 0, 0, 0]]
        self.jezyki = [["angielski", 2], ["polski", 0]]
        self.redukcja_obrazen = redukcjaObrazen
        if self.mod_sila == 3:
            self.redukcja_obrazen += 1
        self.umiejetnosci = [[0], [0, 0, 0, 0, 2], [0, 0, 0, 0, 2], [0, 0, 0, 0, 3], [0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 2], [0, 0, 0, 0, 0], [0, 0, 0, 0, 5], [0, 0, 0, 0, 2], [0, 0, 0, 0, 2],
                             [0, 0, 0, 0, 6], [0, 0, 0, 0, 5], [0, 0, 0, 0, 5], [0, 0, 0, 0, 2], [0, 0, 0, 0, 3],
                             [0, 0, 0, 0, 3], [0, 0, 0, 0, 3], [0, 0, 0, 0, 3], [0, 0, 0, 0, 3], [0, 0, 0, 0, 3],
                             [0, 0, 0, 0, 3], [0, 0, 0, 0, 3], [0, 0, 0, 0, 3], [0, 0, 0, 0, 3], [0, 0, 0, 0, 3],
                             ]
        self.nastaw_umiejetnasci()
        self.planowane_dzialania = []
        self.oslona = 0
        self.w_ruchu = 0

    def nastaw_unik(self):   #todo because of lack of equipment in code implemented.
        self.unik = (self.bazowy_unik + self.umiejetnosci[6][0])


    def aktualny_unik(self):
        return self.unik + self.oslona

    """
    all about dying, but without destroing object.
    """

    def umarl(self):
        self.status = False
        Bot.output(self.imie + " Umarl")

    """
    it's all about allocating wounds. when you have to take a wound, unstoppable in any way (eg from being sick), 
    or after reduction.
    """

    def allokuj(self, obrazenie):
        if obrazenie == 1:
            self.rany[0] += 1
        elif obrazenie == 2:
            self.rany[1] += 1
        elif obrazenie == 3:
            self.rany[0] += 1
        elif obrazenie == 4:
            self.rany[1] += 1
        elif obrazenie == 5:
            self.rany[4][Bot.roll_dice(4) - 1] += 1
        elif obrazenie == 6:
            self.rany[2] += 1
        elif obrazenie == 7:
            self.rany[0] += 1
        elif obrazenie == 8:
            self.rany[4][Bot.roll_dice(4) - 1] += 1
        elif obrazenie == 9:
            self.rany[1] += 1
        elif obrazenie == 10:
            self.rany[1] += 1
            self.allokuj(1)
        elif 10 < obrazenie < 15:
            self.rany[3] += 1
            self.status = False
        elif obrazenie == 15:
            self.umarl()
        if self.rany[0] == self.typ_budowy[0]:
            self.rany[0] = 0
            self.rany[1] += 1
            Bot.output(self.imie + " te drasniecia zabolaly")
        if self.rany[1] == self.typ_budowy[1]:
            self.rany[1] = 0
            self.rany[2] += 1
            Bot.output(self.imie + " to powazna kumulacja")
        if self.rany[2] == self.typ_budowy[2] + 1:
            self.rany[2] = 0
            self.allokuj(11)

    """
    rana
    when it comes to take a wound, but in normal way. You've just been hit, by enemy. 
    then it will resolve damage by you taken.
    """
    def rana(self, rzutNaObrazenia, penetracja=0):
        if penetracja <= self.typ_ochrony:
            rzutNaObrazenia = rzutNaObrazenia - self.redukcja_obrazen
        if rzutNaObrazenia <= 1:
            self.allokuj(1)
            Bot.output(self.imie + " ledwo zostal drasniety")
            return True
        elif rzutNaObrazenia == 2:
            self.allokuj(2)
            Bot.output(self.imie + " odczul")
            return True
        elif rzutNaObrazenia < 6:
            self.allokuj(2)
            self.allokuj(rzutNaObrazenia)
            Bot.output(self.imie + " odczul")
            return True
        elif rzutNaObrazenia == 6:
            self.allokuj(6)
            Bot.output(self.imie + " wyraznie odczul")
            return True
        elif rzutNaObrazenia < 11:
            self.allokuj(6)
            Bot.output(self.imie + " wyraznie odczul")
            self.allokuj(rzutNaObrazenia)
            return True
        elif rzutNaObrazenia < 15:
            self.allokuj(11)
            Bot.output(self.imie + " padl na ziemie")
            return True
        elif rzutNaObrazenia >= 15:
            self.allokuj(15)
            Bot.output(self.imie + " ulegl dezintegracji")
            return

    """
    checks if you can do anything in phase.
    """

    def aktywacja(self, faza):
        if not self.status:
            return False
        if self.mozliwosc_aktywacji[faza] == 1:
            return True
        return False

    """
    counts the penalty to every roll
    """

    def kara(self):
        minus = self.rany[1] * 3 + self.rany[2] * 5
        for i in range(0, len(self.rany[4])):
            if self.rany[4][i] == 1:
                Bot.output("Pamietaj ze ranna jest twoja " + constans.Konczyna[i] + "\n Domyslna dodatkowa kara z tego wynikajaca jest to -4")
        return minus

    """
    stets the modifiers for skills.
    """

    def nastaw_umiejetnasci(self):
        # setting mods for skills.
        for i in range(0, len(self.umiejetnosci)):
            if i == 0:
                continue
            if self.umiejetnosci[i][4] == 1:
                self.umiejetnosci[i][3] = self.mod_sila
            if self.umiejetnosci[i][4] == 2:
                self.umiejetnosci[i][3] = self.modZrecznasc
            if self.umiejetnosci[i][4] == 3:
                self.umiejetnosci[i][3] = self.mod_intelekt
            if self.umiejetnosci[i][4] == 4:
                if self.mod_sila > self.mod_intelekt:
                    self.umiejetnosci[i][3] = self.mod_sila
                else:
                    self.umiejetnosci[i][3] = self.mod_intelekt
            if self.umiejetnosci[i][4] == 5:
                if self.modZrecznasc > self.mod_intelekt:
                    self.umiejetnosci[i][3] = self.modZrecznasc
                else:
                    self.umiejetnosci[i][3] = self.mod_intelekt
            if self.umiejetnosci[i][4] == 6:
                if self.mod_sila > self.modZrecznasc:
                    self.umiejetnosci[i][3] = self.mod_sila
                else:
                    self.umiejetnosci[i][3] = self.modZrecznasc

    """
    it's about testing the skill.
    """

    def rzut_na_umiejetnasc(self, testowana_umiejetnasc, modyfikator = 0):
        umiejka = constans.UmiejetnasciDoInt[testowana_umiejetnasc]
        doRzutu = self.umiejetnosci[umiejka]
        wynik = int(constans.KoscUmiejetnosci[doRzutu[0]] + doRzutu[3] + modyfikator + self.kara())
        return wynik

    """
    heals the wound
    """
    def wylecz(self, typ_rany):

        if typ_rany in ("drasniecie", "lekka rana", "powazna rana", "krytyczna rana", "rana konczyny"):

            return 0
        else:
            Bot.output("nie ma takiej rany!")

    def zaplanuj_akcje(self, komenda):
        self.planowane_dzialania.append(komenda)

    def akcja(self):
        if len(self.planowane_dzialania) == 0:
            self.planowane_dzialania.append("nic")
        wyjscie = self.planowane_dzialania[0]
        self.kara_za_ruch(wyjscie)
        self.planowane_dzialania.pop(0)
        return wyjscie

    def kara_za_ruch(self, dzialanie):
        if dzialanie in ["krok","chod","chód","bieg"]:
            if dzialanie == "krok":
                self.w_ruchu = -1
            if dzialanie in ["chod","chód"]:
                self.w_ruchu = -5
            if dzialanie == "bieg":
                self.w_ruchu = -10
            return True
        self.w_ruchu = 0
        return False

    def zmien_oslone(self, nowa_oslona):
        if nowa_oslona > 10:
            self.oslona = 0
            Bot.output("Nie wałuj! Jeśli zrobiłeś legitnie taką osłonę, zgłoś to na chochlikman@gmail.com, i opisz.")
            return 0
        self.oslona = nowa_oslona
        return self.oslona

