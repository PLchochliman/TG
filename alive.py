"""
it's all about alive objects, which could be destroyed (eg hero, enemy, elephant)
"""

class IstotaZywa:
    status = true
    drasniecia = 0
    lekkaRana = 0
    powaznaRana = 0
    krytycznaRana = 0
    ranaKonczyny[4] = 0


    def kill(self):
        status = false

    def allokuj(self, obrazenie):
        if obrazenie == 1:
            drasniecia =+ 1
        elif obrazenie == 2:
            lekkaRana =+ 1
        elif obrazenie == 3:
            lekkaRana = + 1
        elif obrazenie == 4:
            lekkaRana = + 1
        elif obrazenie == 5:
            lekkaRana = + 1
        elif obrazenie == 6:
            lekkaRana = + 1

        return true

    def rana(self, rzutNaObrazenia):
        if rzutNaObrazenia <= 1:
            allokuj(1)
            return True
        elif rzutNaObrazenia == 2:
            allokuj(2)
            return True
        elif rzutNaObrazenia < 6:
            allokuj(2)
            allokuj(rzutNaObrazenia)
            return True
        elif rzutNaObrazenia == 6:
            allokuj(6)
            return True
        elif rzutNaObrazenia < 11:
            allokuj(6)
            allokuj(rzutNaObrazenia)
            return True
        elif rzutNaObrazenia < 15:
            allokuj(11)
            return True
        elif rzutNaObrazenia >= 15:
            allokuj(15)
            return True
