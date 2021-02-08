import mortal as mortal
import constans as constants
import Bot as system
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
    assert specki[1][0] == "Bron boczna"
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
    system.Output("Bot ran z redukcja obrazen zakonczony")
    wojtek.allokuj(5)
    assert wojtek.kara() == 11
    wojtek.allokuj(14)
    assert not wojtek.aktywacja(2)
    system.Output("zaawansowany Bot aktywacji zakonczony")
    wojtek.allokuj(15)


def testUmiejetnosciIAktywacji(): # test mortal.py
    wojtek = mortal.IstotaZywa(8, 8, 8, "Wojtek")
    assert wojtek.aktywacja(2)
    assert wojtek.umiejetnasci[3][3] == 1
    assert wojtek.umiejetnasci[4][3] == 0
    assert wojtek.rzutNaUmiejetnasc("skupienie") >= 2
    system.Output("umiejetnasci dzialaja")


def testWykupowaniaUmiejetnosciZObnizeniemPrzezSpecjalizacje():
    wojtek = hero.Postac(8, 8, 8, ["Bron boczna", "Karabiny", "Bron krotka"])
    wojtek.wykupRange("obsluga broni")
    assert wojtek.punktyUmiejetnasci == 165
    assert wojtek.umiejetnasci[1][0] == 1
    wojtek.wykupRange("obsluga broni")
    assert wojtek.punktyUmiejetnasci == 164
    assert wojtek.umiejetnasci[1][0] == 2
    wojtek.wykupRange("gadana")
    assert wojtek.punktyUmiejetnasci == 161
    assert wojtek.umiejetnasci[15][0] == 1
    wojtek.wykupRange("prowadzenie pojazdu")
    assert wojtek.punktyUmiejetnasci == 159
    assert wojtek.umiejetnasci[8][0] == 1
    wojtek.wykupRange("gadana")
    assert wojtek.punktyUmiejetnasci == 153
    assert wojtek.umiejetnasci[15][0] == 2
    wojtek.wykupRange("prowadzenie pojazdu")
    assert wojtek.punktyUmiejetnasci == 149
    assert wojtek.umiejetnasci[8][0] == 2
    assert wojtek.rzutNaUmiejetnasc("prowadzenie pojazdu") > 3
    wojtek.podniesPredyspozycje("Bron boczna")
    assert wojtek.umiejetnasci[8][3] == 2
    wojtek.wykupRange("zmysl bitewny")
    assert wojtek.unik == 13
    system.Output("wykupowanie umiejetnasci dziala")

def testJezykow():
    wojtek = hero.Postac(8, 8, 8, ["Bron boczna", "Karabiny", "Bron krotka"])
    wojtek.wykupRange("jezyki")
    assert wojtek.jezyki[0][1] == 3
    system.Output("Jezyki dzialaja")




testLuskaniaDanychZExcela()
testSystemu()
testStalych()
testRanKarSmierci()
testUmiejetnosciIAktywacji()
testWykupowaniaUmiejetnosciZObnizeniemPrzezSpecjalizacje()
testJezykow()
