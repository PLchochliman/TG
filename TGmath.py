import system

"""
wszelkie przeliczanie tego systemu, które jest potrzebne więcej niż 1 raz.
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
