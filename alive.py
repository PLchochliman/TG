"""
it's all about alive objects, which could be destroyed (eg hero, enemy, elephant)
"""
import TGmath
import system


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
    imie = ""

    def __init__(self, Sila, Zrecznasc, Intelekt, imie):
        self.sila = Sila
        self.zrecznasc = Zrecznasc
        self.intelekt = Intelekt
        self.modSila = TGmath.mod(Sila)
        self.modZrecznasc = TGmath.mod(Zrecznasc)
        self.modintelekt = TGmath.mod(Intelekt)
        self.imie = imie

    def umarl(self):
        self.status = False
        system.Output(self.imie + " Umarl")

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
            self.ranaKonczyny[system.rollDice(4)] += 1
        elif obrazenie == 6:
            self.powaznaRana = + 1
        elif obrazenie == 7:
            self.drasniecia = + 1
        elif obrazenie == 8:
            self.ranaKonczyny[system.rollDice(4)] += 1
        elif obrazenie == 9:
            self.lekkaRana = + 1
        elif obrazenie == 10:
            self.allokuj(1)
            self.lekkaRana = + 1
        elif obrazenie < 15:
            self.krytycznaRana = + 1
        elif obrazenie == 15:
            self.umarl()
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
            return


def testZycia():
    wojtek = IstotaZywa(8, 8, 8, "Wojtek")
    wojtek.rana(10)
    assert wojtek.drasniecia == 1
    assert wojtek.lekkaRana == 1
    assert wojtek.powaznaRana == 1
    wojtek.allokuj(15)


testZycia()
