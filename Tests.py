import mortal as mortal
import constans as constants
import system as system
import excelDigger as excelDigger
import hero as hero

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


def testLuskaniaDanychZExcela():
    specki = excelDigger.loader("Specjalizacje.xlsx", ["umiejetnasci"], ["B26"])
    specki = specki.zwroc()
    specki = specki[0]
    assert specki[0][0] == "Bron boczna"
    system.Output("ladowanie z excela dziala")


def testRanKarSmierci(): #testy mortal.py
    wojtek = mortal.IstotaZywa(8, 8, 8, "Wojtek")
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


def testUmiejetnosciIAktywacji(): # test mortal.py
    wojtek = mortal.IstotaZywa(8, 8, 8, "Wojtek")
    assert wojtek.aktywacja(2)
    assert wojtek.Umiejetnasci[3][3] == 1
    assert wojtek.Umiejetnasci[4][3] == 0
    assert wojtek.rzutNaUmiejetnasc("skupienie") >= 2
    system.Output("Umiejetnasci dzialaja")


def testWykupowaniaUmiejetnosci():
    #moze dopisac jeszcze po przypadku dla x2 i x3 (ciche poruszanie i refleks)
    wojtek = hero.Postac(8, 8, 8, ["Bron boczna", "Karabiny", "Karabiny maszynowe"])
    wojtek.wykupRange("obsluga broni")
    assert wojtek.punktyUmiejetnasci == 165
    assert wojtek.Umiejetnasci[1][0] == 1
    wojtek.wykupRange("obsluga broni")
    assert wojtek.punktyUmiejetnasci == 164
    assert wojtek.Umiejetnasci[1][0] == 2
    wojtek.wykupRange("ciche poruszanie")
    assert wojtek.punktyUmiejetnasci == 161
    assert wojtek.Umiejetnasci[7][0] == 1
    wojtek.wykupRange("refleks")
    assert wojtek.punktyUmiejetnasci == 159
    assert wojtek.Umiejetnasci[2][0] == 1
    system.Output("wykupowanie umiejetnasci dziala")


testLuskaniaDanychZExcela()
testSystemu()
testStalych()
testRanKarSmierci()
testUmiejetnosciIAktywacji()
