import system


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
