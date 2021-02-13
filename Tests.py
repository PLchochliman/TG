import mortal as mortal
import constans as constants
import Bot as Bot
import excelDigger as excelDigger
import hero as hero
import items as items

"""
it all should be made by another 
"""


def test_systemu():
    assert Bot.roll_dice(4) > 0
    assert Bot.roll_dice(4) < 5
    assert len(Bot.multi_roll_dice(4, 5)) < 6
    assert len(Bot.multi_roll_dice(4, 5)) > 4
    assert Bot.sum_multi_roll_dice(4, 5) > 4
    assert Bot.sum_multi_roll_dice(4, 5) < 21
    assert Bot.roll_dice_from_text("4D6") > 3
    assert Bot.roll_dice_from_text("4D6") < 25
    assert Bot.roll_dice_from_text("D6") < 7
    assert Bot.roll_dice_from_text("D6") > 0
    Bot.output("System działa bez zarzutów")


def test_stalych():
    assert constants.mod(10) == 2
    assert constants.mod(5) == 0
    assert constants.KoscUmiejetnosci[1] > 2
    Bot.output("matematyka TG dziala bez zarzutu")


def test_luskania_danych_z_excela():
    specki = excelDigger.loader("Specjalizacje.xlsx", ["umiejetnasci"], ["B26"])
    specki = specki.zwroc()
    specki = specki[0]
    assert specki[1][0] == "bron boczna"
    Bot.output("ladowanie z excela dziala")


def test_ran_kar_smierci(): #testy mortal.py
    wojtek = mortal.IstotaZywa(8, 8, 8, "Wojtek")
    wojtek.rana(10, 0)
    assert wojtek.drasniecia == 1
    assert wojtek.lekkaRana == 1
    assert wojtek.powaznaRana == 1
    Bot.output("podstawowy test Ran zakonczony")
    wojtek.redukcjaObrazen = 2
    wojtek.rana(3, 0)
    assert wojtek.drasniecia == 2
    assert wojtek.lekkaRana == 1
    wojtek.rana(3, 0)
    wojtek.rana(3, 0)
    assert wojtek.lekkaRana == 2
    Bot.output("Bot ran z redukcja obrazen zakonczony")
    wojtek.allokuj(5)
    assert wojtek.kara() == 11
    wojtek.allokuj(14)
    assert not wojtek.aktywacja(2)
    Bot.output("zaawansowany Bot aktywacji zakonczony")
    wojtek.allokuj(15)


def test_umiejetnosci_i_aktywacji(): # test mortal.py
    wojtek = mortal.IstotaZywa(8, 8, 8, "Wojtek")
    assert wojtek.aktywacja(2)
    assert wojtek.umiejetnasci[3][3] == 1
    assert wojtek.umiejetnasci[4][3] == 0
    assert wojtek.rzut_na_umiejetnasc("skupienie") >= 2
    Bot.output("umiejetnasci dzialaja")


def test_wykupowania_umiejetnosci_z_obnizeniem_przez_specjalizacje():
    wojtek = hero.Postac(8, 8, 8, ["bron boczna", "karabiny", "bron krotka"])
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
    wojtek.podnies_predyspozycje("bron boczna")
    assert wojtek.umiejetnasci[8][3] == 2
    wojtek.wykup_range("zmysl bitewny")
    assert wojtek.unik == 13
    Bot.output("wykupowanie umiejetnasci dziala")


def test_jezykow():
    wojtek = hero.Postac(8, 8, 8, ["bron boczna", "karabiny", "bron krotka"])
    wojtek.wykup_range("jezyki")
    assert wojtek.jezyki[0][1] == 3
    Bot.output("Jezyki dzialaja")


def test_przedmiotow():
    itemki = items.Przedmioty('')
    m4ka = itemki.luskacz_broni("m4a1")
    assert m4ka[6] == 'ś'
    nozyk = itemki.luskacz_broni_bialej("nóż")
    assert nozyk[3] == 3
    hek = itemki.luskacz_granatow("granat ofensywny")
    assert hek[2] == "2d6"
    acog = itemki.luskacz_celownikow("acogx4")
    assert acog[3] == 10
    trijcon = itemki.luskacz_celownikow("trijcon")
    assert trijcon[4] == "strzelby"
    Bot.output("przedmioty dzialaja")


def test_dzialania_broni():
    wojtek = hero.Postac(8, 8, 8, ["bron boczna", "karabiny", "bron krotka"])
    cel = hero.Postac(8, 8, 8, ["bron boczna", "karabiny", "bron krotka"])
    giwera = items.Bron("strzelectwo", "2D2", 11, "m")
    giwera.atakuj(wojtek, cel, 5)
    assert cel.lekkaRana > 0
    giwera2 = items.Bron("strzelectwo", "2D2", -5, "ś")
    giwera2.atakuj(cel, wojtek, 2)
    assert wojtek.lekkaRana == 0
    Bot.output("podstawowa Bron dziala")

def test_dzialania_broni_strzeleckiej():
    itemki = items.Przedmioty('')
    m4ka = itemki.luskacz_broni("m4a1")
    M4KA = items.BronStrzelecka(m4ka)
    wojtek = hero.Postac(8, 8, 8, ["bron boczna", "karabiny", "bron krotka"])
    beben = hero.Postac(8, 8, 8, ["bron boczna", "karabiny", "bron krotka"])
    M4KA.atakuj(wojtek, beben)
    Bot.output("TEN TEST BRONI STRZELECKIEJ JEST NEDOROBIONY!")


test_luskania_danych_z_excela()
test_systemu()
test_stalych()
test_ran_kar_smierci()
test_umiejetnosci_i_aktywacji()
test_wykupowania_umiejetnosci_z_obnizeniem_przez_specjalizacje()
test_jezykow()
test_przedmiotow()
test_dzialania_broni()
test_dzialania_broni_strzeleckiej()
