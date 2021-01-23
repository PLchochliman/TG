"""
it's all about alive objects, which could be destroyed (eg hero, enemy, elephant)
"""




class IstotaZywa:

    sila, zrecznasc, intelekt = 0
    modSila, modZrecznosc, modInt = 0
    status = true
    drasniecia = 0
    lekkaRana = 0
    powaznaRana = 0
    krytycznaRana = 0
    ranaKonczyny[4] = 0

    def mod(self, statystyka):
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
            return false


        return True

    def __init__(self, Sila, Zrecznasc, Intelekt):
        sila = Sila
        zrecznasc = Zrecznasc
        intelekt = Intelekt


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

