import mortal as mortal
import constans as constants
import system as system
import excelDigger as excelDigger


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


def testStalych():
    assert constants.mod(10) == 2
    assert constants.mod(5) == 0
    assert constants.KoscUmiejetnosci[1] > 2
    system.Output("matematyka TG dziala bez zarzutu")


def testZycia():
    wojtek = mortal.IstotaZywa(8, 8, 8, "Wojtek")
    assert wojtek.aktywacja(2) == True
    wojtek.rana(10, 0)
    assert wojtek.drasniecia == 1
    assert wojtek.lekkaRana == 1
    assert wojtek.powaznaRana == 1
    system.Output("podstawowy test Ran zakonczony")
    wojtek.redukcjaObrazen = 2
    wojtek.rana(3, 0)
    assert wojtek.drasniecia == 2
    assert wojtek.lekkaRana == 1
    wojtek.rana(3, 0)
    wojtek.rana(3, 0)
    assert wojtek.lekkaRana == 2
    system.Output("system ran z redukcja obrazen zakonczony")
    wojtek.allokuj(5)
    assert wojtek.kara() == 11
    wojtek.allokuj(14)
    assert wojtek.aktywacja(2) == False
    system.Output("zaawansowany system aktywacji zakonczony")
    wojtek.allokuj(15)

def TestLuskaniaDanychZExcela():
    specki = excelDigger.loader("Specjalizacje.xlsx", ["umiejetnasci"], ["B26"])
    specki = specki.zwroc()
    specki = specki[0]
    assert specki[0][0] == "Bron boczna"
    system.Output("ladowanie z excela dziala")



testSystemu()
testStalych()
testZycia()
TestLuskaniaDanychZExcela()
