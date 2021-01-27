import mortal as mortal
import system as system
import constans as constans
"starting creating real character"


class Postac(mortal.IstotaZywa):
    punktyUmiejetnasci = 0
    pieniadze = 0
    wyposazenie_zalozone = ["", "", "", "", "", "", "", ""]     #states for Head, torso (tactical vest), belt, leg panel1, legpanel2, backpack, backpackslot1, backpackslot2
    specjalizacje = [0, 0, 0]


    def __init__(self, sila, zrecznasc, intelekt, imie="bob", pu=150, kasa=9000):
        super().__init__(sila, zrecznasc, intelekt, imie)
        self.punktyUmiejetnasci = pu + pu / 10 * self.modIntelekt
        self.pieniadze = kasa



    def wybierzSpecjalizacje(self):
        for i in self.specjalizacje:
            if i == 0:
                system.Output("wybierz specjalizacje")

wojtek = Postac(8, 8, 8)