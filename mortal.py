"""
it's all about alive objects, which could be destroyed (eg hero, enemy, elephant)
"""
import Bot
import constans


class IstotaZywa: #pełne pokrycie
    sila, zrecznasc, intelekt = 0, 0, 0,
    mod_sila, mod_zrecznosc, mod_intelekt = 0, 0, 0,
    status = True
    drasniecia, lekka_rana, powazna_rana, krytyczna_rana = 0, 0, 0, 0,
    rana_konczyny = [0, 0, 0, 0]
    redukcja_obrazen, typ_ochrony = 0, 0
    imie = ""
    typ_budowy = []
    mozliwosc_aktywacji = []
    bazowy_unik = 10
    unik = 10
    punktyWytrwalosci, przeznaczenie = 0, 0,
    udzwig = 0
    umiejetnasci = constans.Umiejetnasci
    jezyki = [["angielski", 2], ["polski", 0]]

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
        self.redukcja_obrazen = redukcjaObrazen
        if self.mod_sila == 3:
            self.redukcja_obrazen += 1
        self.nastaw_umiejetnasci()

    def nastaw_unik(self):   #todo because of lack of equipment in code implemented.
        self.unik = (self.bazowy_unik + self.umiejetnasci[6][0])

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
            self.drasniecia += 1
        elif obrazenie == 2:
            self.lekka_rana += 1
        elif obrazenie == 3:
            self.drasniecia += 1
        elif obrazenie == 4:
            self.lekka_rana += 1
        elif obrazenie == 5:
            self.rana_konczyny[Bot.roll_dice(4) - 1] += 1
        elif obrazenie == 6:
            self.powazna_rana += 1
        elif obrazenie == 7:
            self.drasniecia += 1
        elif obrazenie == 8:
            self.rana_konczyny[Bot.roll_dice(4) - 1] += 1
        elif obrazenie == 9:
            self.lekka_rana += 1
        elif obrazenie == 10:
            self.allokuj(1)
            self.lekka_rana += 1
        elif obrazenie < 15:
            self.krytyczna_rana += 1
            self.status = False
        elif obrazenie == 15:
            self.umarl()
        if self.drasniecia == self.typ_budowy[0]:
            self.drasniecia = 0
            self.lekka_rana += 1
            Bot.output(self.imie + " te drasniecia zabolaly")
        if self.lekka_rana == self.typ_budowy[1]:
            self.lekka_rana = 0
            self.powazna_rana += 1
            Bot.output(self.imie + " to powazna kumulacja")
        if self.powazna_rana == self.typ_budowy[2] + 1:
            self.powazna_rana = 0
            self.allokuj(11)

    """
    rana
    when it comes to take a wound, but in normal way. You've just been hit, by enemy. 
    then it will resolve damage by you taken.
    """
    def rana(self, rzutNaObrazenia, penetracja):
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

    def kara(self):
        minus = self.lekka_rana * 3 + self.powazna_rana * 5
        for i in range(0, len(self.rana_konczyny)):
            if self.rana_konczyny[i] == 1:
                Bot.output("Pamietaj ze ranna jest twoja " + constans.Konczyna[i] + "\n Domyslna dodatkowa kara z tego wynikajaca jest to -4")
        return minus

    def nastaw_umiejetnasci(self):
        # setting mods for skills.
        for i in range(0, len(self.umiejetnasci)):
            if i == 0:
                continue
            if self.umiejetnasci[i][4] == 1:
                self.umiejetnasci[i][3] = self.mod_sila
            if self.umiejetnasci[i][4] == 2:
                self.umiejetnasci[i][3] = self.modZrecznasc
            if self.umiejetnasci[i][4] == 3:
                self.umiejetnasci[i][3] = self.mod_intelekt
            if self.umiejetnasci[i][4] == 4:
                if self.mod_sila > self.mod_intelekt:
                    self.umiejetnasci[i][3] = self.mod_sila
                else:
                    self.umiejetnasci[i][3] = self.mod_intelekt
            if self.umiejetnasci[i][4] == 5:
                if self.modZrecznasc > self.mod_intelekt:
                    self.umiejetnasci[i][3] = self.modZrecznasc
                else:
                    self.umiejetnasci[i][3] = self.mod_intelekt
            if self.umiejetnasci[i][4] == 6:
                if self.mod_sila > self.modZrecznasc:
                    self.umiejetnasci[i][3] = self.mod_sila
                else:
                    self.umiejetnasci[i][3] = self.modZrecznasc

    def rzut_na_umiejetnasc(self, testowana_umiejetnasc):
        umiejka = constans.UmiejetnasciDoInt[testowana_umiejetnasc]
        doRzutu = self.umiejetnasci[umiejka]
        return constans.KoscUmiejetnosci[doRzutu[0]] + doRzutu[3]

    """
        umiejetnasci is table for skills. from constants you 
    first states for skill level, second for Cost, 
    3rd of specializations (Cost is depending on it), 
    4th is for all modifiers from predispositions (skill in specialisations)and modifiers from stats
    5th is all for modifier based on base stats modifier.
    """
