import mortal as mortal
import system as system
import constans as constans
"starting creating real character"


class Postac(mortal.IstotaZywa):
    punktyUmiejetnasci = 0
    pieniadze = 0
    wyposazenie_zalozone = ["", "", "", "", "", "", "", ""]     #states for Head, torso (tactical vest), belt, leg panel1, legpanel2, backpack, backpackslot1, backpackslot2
    specjalizacje = [0, 0, 0]
    """
    umiejetnasci is table for skills. from constants you 
    first states for skill level, second for Cost, 
    3rd of specializations (Cost is dependingo for it), 
    4th is for all modifiers from predispositions (skill in specialisations)
    5th is all for modifier based on base stats modifier. 0 states for none, 1 is for Power, 2 is for Dexerity, 3 is
    for Inteligence, 4 is for Power or Inteligence, 5 is for Dexerity or Inteligence, 6 is for Power or Dexerity.
    """

    Umiejetnasci = [[0],
                    [0, 0, 0, 0, 2],
                    [0, 0, 0, 0, 2],
                    [0, 0, 0, 0, 3],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 2],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 5],
                    [0, 0, 0, 0, 2], #prowadzeinie pojazdu
                    [0, 0, 0, 0, 2],
                    [0, 0, 0, 0, 6],
                    [0, 0, 0, 0, 5],
                    [0, 0, 0, 0, 5],
                    [0, 0, 0, 0, 2],
                    [0, 0, 0, 0, 3],
                    [0, 0, 0, 0, 3],
                    [0, 0, 0, 0, 3],
                    [0, 0, 0, 0, 3], #nastepne sa juz odmianami dyscypliny naukowej itd.
                    [0, 0, 0, 0, 3],
                    [0, 0, 0, 0, 3],
                    [0, 0, 0, 0, 3],
                    [0, 0, 0, 0, 3],
                    [0, 0, 0, 0, 3],
                    [0, 0, 0, 0, 3],
                    [0, 0, 0, 0, 3],
                    ]

    def __init__(self, sila, zrecznasc, intelekt, imie="bob", pu=150, kasa=9000):
        super().__init__(sila, zrecznasc, intelekt, imie)
        self.punktyUmiejetnasci = pu + pu / 10 * self.modIntelekt
        self.pieniadze = kasa

    def wybierzSpecjalizacje(self):
        for i in self.specjalizacje:
            if i == 0:
                system.Output("wybierz specjalizacje")



wojtek = Postac(8,8,8)