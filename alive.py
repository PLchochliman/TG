"""
it's all about alive objects, which could be destroyed (eg hero, enemy, elephant)
"""
import TGmath
import system

"""
mod counts the modificator of statistics
"""
"""
def mod(statystyka):
    if statystyka < 3:
        return -2
    if statystyka < 5:
        return -1
    if statystyka < 8:
        return 0
    if statystyka < 10:
        return 1
    if statystyka < 12:
        return 2
    if statystyka == 13:
        return 3
    if statystyka > 13:
        system.Output("coś dużo tego. chyba to potwór \n  Jeśli nie jesteś mutantem, zmień to natychmiast")
        return 4
"""


class IstotaZywa:
    sila, zrecznasc, intelekt = 0
    modSila, modZrecznosc, modIntelekt = 0
    status = True
    drasniecia = 0
    lekkaRana = 0
    powaznaRana = 0
    krytycznaRana = 0
    ranaKonczyny = [0, 0, 0, 0]
    redukcjaObrazen = 0

    def __init__(self, Sila, Zrecznasc, Intelekt):
        self.sila = Sila
        self.zrecznasc = Zrecznasc
        self.intelekt = Intelekt
        self.modSila = TGmath.mod(Sila)
        self.modZrecznasc = TGmath.mod(Zrecznasc)
        self.modintelekt = TGmath.mod(Intelekt)

    def umarl(self):
        self.status = False

    def allokuj(self, obrazenie):
        if obrazenie == 1:
            self.drasniecia = + 1
        elif obrazenie == 2:
            self.lekkaRana = + 1
        elif obrazenie == 3:
            self.drasniecia = + 1
        elif obrazenie == 4:
            self.lekkaRana = + 1
        elif obrazenie == 5:
            self.ranaKonczyn[system.rollDice(4)] = +1
        elif obrazenie == 6:
            self.lekkaRana = + 1
        return True

    def rana(self, rzutNaObrazenia):
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
            return True
