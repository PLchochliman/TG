"""
it's all about alive objects, which could be destroyed (eg hero, enemy, elephant)
"""
import Bot
import constans


class IstotaZywa:
    sila, zrecznasc, intelekt = 0, 0, 0,
    modSila, modZrecznosc, modIntelekt = 0, 0, 0,
    status = True
    drasniecia, lekkaRana, powaznaRana, krytycznaRana = 0, 0, 0, 0,
    ranaKonczyny = [0, 0, 0, 0]
    redukcjaObrazen, typOchrony = 0, 0
    imie = ""
    typBudowy = []
    mozliwoscAktywacji = []
    bazowyUnik = 10
    unik = 10
    punktyWytrwalosci, przeznaczenie = 0, 0,
    udzwig = 0
    umiejetnasci = constans.Umiejetnasci
    jezyki = [["angielski", 2], ["polski", 0]]

    def __init__(self, sila, zrecznasc, intelekt, imie="bot", unik=10, redukcjaObrazen=0, typOchrony=0):
        self.sila = sila
        self.zrecznasc = zrecznasc
        self.intelekt = intelekt
        self.modSila = constans.mod(sila)
        self.modZrecznasc = constans.mod(zrecznasc)
        self.modIntelekt = constans.mod(intelekt)
        self.imie = imie
        self.typBudowy = constans.TypBudowy[self.modSila]
        self.mozliwoscAktywacji = constans.TypyAktywacji[self.modZrecznasc]
        self.bazowyUnik = unik + self.modZrecznasc + self.modIntelekt
        self.unik = self.bazowyUnik         #na razie jest bez sensu, ale w późniejszych rozrachunkach bedzie potrzebne
        self.punktyWytrwalosci = self.intelekt * 2
        self.przeznaczenie = self.modIntelekt + 1
        self.typOchrony = typOchrony
        self.udzwig = self.sila * 5
        self.redukcjaObrazen = redukcjaObrazen
        if self.modSila == 3:
            self.redukcjaObrazen += 1
        self.nastawUmiejetnasci()

    def nastawUnik(self):   #todo because of lack of equipment in code implemented.
        self.unik = (self.bazowyUnik + self.umiejetnasci[6][0])


    """
    all about dying, but without destroing object.
    """

    def umarl(self):
        self.status = False
        Bot.Output(self.imie + " Umarl")

    """
    it's all about allocating wounds. when you have to take a wound, unstoppable in any way (eg from being sick), 
    or after reduction.
    """

    def allokuj(self, obrazenie):
        if obrazenie == 1:
            self.drasniecia += 1
        elif obrazenie == 2:
            self.lekkaRana += 1
        elif obrazenie == 3:
            self.drasniecia += 1
        elif obrazenie == 4:
            self.lekkaRana += 1
        elif obrazenie == 5:
            self.ranaKonczyny[Bot.rollDice(4) - 1] += 1
        elif obrazenie == 6:
            self.powaznaRana += 1
        elif obrazenie == 7:
            self.drasniecia += 1
        elif obrazenie == 8:
            self.ranaKonczyny[Bot.rollDice(4) - 1] += 1
        elif obrazenie == 9:
            self.lekkaRana += 1
        elif obrazenie == 10:
            self.allokuj(1)
            self.lekkaRana += 1
        elif obrazenie < 15:
            self.krytycznaRana += 1
            self.status = False
        elif obrazenie == 15:
            self.umarl()
        if self.drasniecia == self.typBudowy[0]:
            self.drasniecia = 0
            self.lekkaRana += 1
        if self.lekkaRana == self.typBudowy[1]:
            self.lekkaRana = 0
            self.powaznaRana += 1
        if self.powaznaRana == self.typBudowy[2] + 1:
            self.powaznaRana = 0
            self.allokuj(11)

    """
    rana
    when it comes to take a wound, but in normal way. You've just been hit, by enemy. 
    then it will resolve damage by you taken.
    """
    def rana(self, rzutNaObrazenia, penetracja):
        if penetracja <= self.typOchrony:
            rzutNaObrazenia = rzutNaObrazenia - self.redukcjaObrazen
        if rzutNaObrazenia <= 1:
            self.allokuj(1)
            return True
        elif rzutNaObrazenia == 2:
            self.allokuj(2)
            return True
        elif rzutNaObrazenia < 6:
            self.allokuj(2)
            self.allokuj(rzutNaObrazenia)
            return True
        elif rzutNaObrazenia == 6:
            self.allokuj(6)
            return True
        elif rzutNaObrazenia < 11:
            self.allokuj(6)
            self.allokuj(rzutNaObrazenia)
            return True
        elif rzutNaObrazenia < 15:
            self.allokuj(11)
            return True
        elif rzutNaObrazenia >= 15:
            self.allokuj(15)
            return

    """
    checks if you can do anything in phase.
    """

    def aktywacja(self, faza):
        if not self.status:
            return False
        if self.mozliwoscAktywacji[faza] == 1:
            return True
        return False

    def kara(self):
        minus = self.lekkaRana * 3 + self.powaznaRana * 5
        for i in range(0, len(self.ranaKonczyny)):
            if self.ranaKonczyny[i] == 1:
                Bot.Output("Pamietaj ze ranna jest twoja " + constans.Konczyna[i] + "\n Domyslna dodatkowa kara z tego wynikajaca jest to -4")
        return minus

    def nastawUmiejetnasci(self):
        # setting mods for skills.
        for i in range(0, len(self.umiejetnasci)):
            if i == 0:
                continue
            if self.umiejetnasci[i][4] == 1:
                self.umiejetnasci[i][3] = self.modSila
            if self.umiejetnasci[i][4] == 2:
                self.umiejetnasci[i][3] = self.modZrecznasc
            if self.umiejetnasci[i][4] == 3:
                self.umiejetnasci[i][3] = self.modIntelekt
            if self.umiejetnasci[i][4] == 4:
                if self.modSila > self.modIntelekt:
                    self.umiejetnasci[i][3] = self.modSila
                else:
                    self.umiejetnasci[i][3] = self.modIntelekt
            if self.umiejetnasci[i][4] == 5:
                if self.modZrecznasc > self.modIntelekt:
                    self.umiejetnasci[i][3] = self.modZrecznasc
                else:
                    self.umiejetnasci[i][3] = self.modIntelekt
            if self.umiejetnasci[i][4] == 6:
                if self.modSila > self.modZrecznasc:
                    self.umiejetnasci[i][3] = self.modSila
                else:
                    self.umiejetnasci[i][3] = self.modZrecznasc

    def rzutNaUmiejetnasc(self, testowanaUmiejetnasc):
        umiejka = constans.UmiejetnasciDoInt[testowanaUmiejetnasc]
        doRzutu = self.umiejetnasci[umiejka]
        return constans.KoscUmiejetnosci[doRzutu[0]] + doRzutu[3]

    """
        umiejetnasci is table for skills. from constants you 
    first states for skill level, second for Cost, 
    3rd of specializations (Cost is depending on it), 
    4th is for all modifiers from predispositions (skill in specialisations)and modifiers from stats
    5th is all for modifier based on base stats modifier.
    """
