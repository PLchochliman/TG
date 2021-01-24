
from . import alive
from . import TGmath
from . import system


"""
it all should be made by another 
"""


def testSystemu():
    assert system.rollDice(4) > 0
    assert system.rollDice(4) < 5
    assert len(system.multiRollDice(4, 5)) < 6
    assert len(system.multiRollDice(4, 5)) > 4
    assert system.sumMultiRollDice(4, 5) > 4
    assert system.sumMultiRollDice(4, 5) < 21
    system.Output("System działa bez zarzutów")


def testTGmath():
    assert TGmath.mod(10) == 2
    assert TGmath.mod(5) == 0
    assert TGmath.KoscUmiejetnosci[1] > 2
    system.Output("matematyka TG dziala bez zarzutu")


def testZycia():
    wojtek = alive.IstotaZywa(8, 8, 8, "Wojtek")
    wojtek.rana(10)
    assert wojtek.drasniecia == 1
    assert wojtek.lekkaRana == 1
    assert wojtek.powaznaRana == 1
    wojtek.allokuj(15)


testSystemu()
testTGmath()
testZycia()
