import alive as alive

"starting creating real character"

class Postac(alive.IstotaZywa):
    punktyUmiejetnasci = 0
    pieniadze = 0

    def __init__(self, sila, zrecznasc, intelekt, imie="bob", pu=150, kasa=9000):
        super().__init__(sila, zrecznasc, intelekt, imie)
        self.punktyUmiejetnasci = pu + pu / 10 * self.modIntelekt
        self.pieniadze = kasa
