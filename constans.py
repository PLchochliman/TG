import system

"""
COnstans are not tested!!!!
Only by the way of other tests
"""


"""
all about Hardness of body.
1st column is slight wound (drasniecie) 2nd is for light wounds, 3rd states for serious injury 
"""

TypBudowy = {
    -3: [1, 1, 1],
    -2: [2, 1, 1],
    -1: [2, 2, 1],
    0: [3, 2, 1],
    1: [4, 3, 1],
    2: [5, 4, 1],
    3: [5, 4, 1],
    4: [5, 4, 2]
}

Umiejetnosci = {
    1: "Obsluga broni",
    2: "Refleks",
    3: "Skupienie",
    4: "Strzelectwo",
    5: "Walka wrecz",
    6: "Zmysl bitewny",
    7: "Ciche poruszanie",
    8: "Prowadzenie pojazdu",
    9: "Spostrzeganie",
    10: "Sprawnosc fizyczna",
    11: "Survival",
    12: "Ukrywanie",
    13: "Zreczne palce",
    14: "Dyscyplina Naukowa",
    15: "Gadana",
    16: "Jezyki",
    17: "Zawod",
    18: "Dyscyplina Naukowa Medycyna",
    19: "Dyscyplina Naukowa Informatyka",
    20: "Dyscyplina Naukowa Humanistyka",
    21: "Zawod Rusznikarz",
    22: "Zawod Kowal",
    23: "Zawod Mechanik",
    24: "Zawod Kucharz"
}

"""
    umiejetnasci is table for skills. from constants you 
    first states for skill level, second for Cost, 
    3rd of specializations (Cost is dependingo for it), 
    4th is for all modifiers from predispositions (skill in specialisations)and modifiers from stats
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

"""
It's providing table of activation
"""

TypyAktywacji = {
    -3: [0, 0, 0, 0, 0, 1],
    -2: [0, 1, 0, 0, 0, 0],
    -1: [0, 1, 0, 0, 1, 0],
    0: [0, 1, 0, 1, 0, 1],
    1: [0, 1, 1, 0, 1, 1],
    2: [0, 1, 1, 1, 1, 1],
    3: [1, 1, 1, 1, 1, 1],
}

""""
for purposes of limb injury
"""

Konczyna = {
    0: "prawa reka",
    1: "lewa reka",
    2: "prawa noga",
    3: "lewa noga"
}




"""
when need to skill roll based on skill level.
"""

KoscUmiejetnosci = {
    0: system.rollDice(6),
    1: system.rollDice(6) + 2,
    2: system.sumMultiRollDice(6, 2) + 2,
    3: system.sumMultiRollDice(6, 2) + 4,
    4: system.sumMultiRollDice(6, 3) + 4,
    5: system.sumMultiRollDice(6, 3) + 6,
    6: system.sumMultiRollDice(6, 4) + 6,
}

"""
racalculating statistics into modifiers to roll.
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
wszelkie przeliczanie tego systemu, które jest potrzebne więcej niż 1 raz.
"""
