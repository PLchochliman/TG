import mortal as mortal
import constans as constants
import Bot as system
import excelDigger as excelDigger
import hero as hero
import items as items

"""
it all should be made by another 
"""


def test_systemu():
    assert system.roll_dice(4) > 0
    assert system.roll_dice(4) < 5
    assert len(system.multi_roll_dice(4, 5)) < 6
    assert len(system.multi_roll_dice(4, 5)) > 4
    assert system.sum_multi_roll_dice(4, 5) > 4
    assert system.sum_multi_roll_dice(4, 5) < 21
    system.output("System działa bez zarzutów")


def test_stalych():
    assert constants.mod(10) == 2
    assert constants.mod(5) == 0
    assert constants.KoscUmiejetnosci[1] > 2
    system.output("matematyka TG dziala bez zarzutu")


def test_luskania_danych_z_excela():
    specki = excelDigger.loader("Specjalizacje.xlsx", ["umiejetnasci"], ["B26"])
    specki = specki.zwroc()
    specki = specki[0]
    assert specki[1][0] == "Bron boczna"
    system.output("ladowanie z excela dziala")


def test_ran_kar_smierci(): #testy mortal.py
    wojtek = mortal.IstotaZywa(8, 8, 8, "Wojtek")
    wojtek.rana(10, 0)
    assert wojtek.drasniecia == 1
    assert wojtek.lekkaRana == 1
    assert wojtek.powaznaRana == 1
    system.output("podstawowy test Ran zakonczony")
    wojtek.redukcjaObrazen = 2
    wojtek.rana(3, 0)
    assert wojtek.drasniecia == 2
    assert wojtek.lekkaRana == 1
    wojtek.rana(3, 0)
    wojtek.rana(3, 0)
    assert wojtek.lekkaRana == 2
    system.output("Bot ran z redukcja obrazen zakonczony")
    wojtek.allokuj(5)
    assert wojtek.kara() == 11
    wojtek.allokuj(14)
    assert not wojtek.aktywacja(2)
    system.output("zaawansowany Bot aktywacji zakonczony")
    wojtek.allokuj(15)


def test_umiejetnosci_i_aktywacji(): # test mortal.py
    wojtek = mortal.IstotaZywa(8, 8, 8, "Wojtek")
    assert wojtek.aktywacja(2)
    assert wojtek.umiejetnasci[3][3] == 1
    assert wojtek.umiejetnasci[4][3] == 0
    assert wojtek.rzut_na_umiejetnasc("skupienie") >= 2
    system.output("umiejetnasci dzialaja")


def test_wykupowania_umiejetnosci_z_obnizeniem_przez_specjalizacje():
    wojtek = hero.Postac(8, 8, 8, ["Bron boczna", "Karabiny", "Bron krotka"])
    wojtek.wykup_range("obsluga broni")
    assert wojtek.punktyUmiejetnasci == 165
    assert wojtek.umiejetnasci[1][0] == 1
    wojtek.wykup_range("obsluga broni")
    assert wojtek.punktyUmiejetnasci == 164
    assert wojtek.umiejetnasci[1][0] == 2
    wojtek.wykup_range("gadana")
    assert wojtek.punktyUmiejetnasci == 161
    assert wojtek.umiejetnasci[15][0] == 1
    wojtek.wykup_range("prowadzenie pojazdu")
    assert wojtek.punktyUmiejetnasci == 159
    assert wojtek.umiejetnasci[8][0] == 1
    wojtek.wykup_range("gadana")
    assert wojtek.punktyUmiejetnasci == 153
    assert wojtek.umiejetnasci[15][0] == 2
    wojtek.wykup_range("prowadzenie pojazdu")
    assert wojtek.punktyUmiejetnasci == 149
    assert wojtek.umiejetnasci[8][0] == 2
    assert wojtek.rzut_na_umiejetnasc("prowadzenie pojazdu") > 3
    wojtek.podnies_predyspozycje("Bron boczna")
    assert wojtek.umiejetnasci[8][3] == 2
    wojtek.wykup_range("zmysl bitewny")
    assert wojtek.unik == 13
    system.output("wykupowanie umiejetnasci dziala")


def test_jezykow():
    wojtek = hero.Postac(8, 8, 8, ["Bron boczna", "Karabiny", "Bron krotka"])
    wojtek.wykup_range("jezyki")
    assert wojtek.jezyki[0][1] == 3
    system.output("Jezyki dzialaja")


def test_przedmiotow():
    itemki = items.Przedmioty('kurwa')
    m4ka = itemki.luskacz_broni("M4A1")
    assert m4ka[6] == 'Ś'


test_luskania_danych_z_excela()
test_systemu()
test_stalych()
test_ran_kar_smierci()
test_umiejetnosci_i_aktywacji()
test_wykupowania_umiejetnosci_z_obnizeniem_przez_specjalizacje()
test_jezykow()
test_przedmiotow()
