import system

"""
COnstans are not tested!!!!
Only by the way of other tests
"""


"""
all about Hardness of body.
1st column is slight wound (drasniecie) 2nd is for light wounds, 3rd states for serious injury 
transformed into tuple, due to optimalisation.
"""

TypBudowy = {
    -3: (1, 1, 1),
    -2: (2, 1, 1),
    -1: (2, 2, 1),
    0: (3, 2, 1),
    1: (4, 3, 1),
    2: (5, 4, 1),
    3: (5, 4, 1),
    4: (5, 4, 2)
}

Umiejetnosci = {
    1: "obsluga broni",
    2: "refleks",
    3: "skupienie",
    4: "strzelectwo",
    5: "walka wrecz",
    6: "zmysl bitewny",
    7: "ciche poruszanie",
    8: "prowadzenie pojazdu",
    9: "spostrzeganie",
    10: "sprawnosc fizyczna",
    11: "survival",
    12: "ukrywanie",
    13: "zreczne palce",
    14: "dyscyplina naukowa",
    15: "gadana",
    16: "jezyki",
    17: "zawod",
    18: "dyscyplina naukowa Medycyna",
    19: "dyscyplina naukowa Informatyka",
    20: "dyscyplina naukowa Humanistyka",
    21: "zawod Rusznikarz",
    22: "zawod Kowal",
    23: "zawod Mechanik",
    24: "zawod Kucharz"
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
It's providing table of activation. Made into tuple, for optimalisation cause.
"""

TypyAktywacji = {
    -3: (0, 0, 0, 0, 0, 1),
    -2: (0, 1, 0, 0, 0, 0),
    -1: (0, 1, 0, 0, 1, 0),
    0: (0, 1, 0, 1, 0, 1),
    1: (0, 1, 1, 0, 1, 1),
    2: (0, 1, 1, 1, 1, 1),
    3: (1, 1, 1, 1, 1, 1),
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
