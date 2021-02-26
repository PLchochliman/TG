import mortal as mortal
import constans as constants
import Bot as Bot
import excelDigger as excelDigger
import hero as hero
import items_old as items_old
import items as items
import mechanics as mechanics


def sprawdz_jak_cel_oberwal(cel):
    if cel.lekka_rana == 0:
        if cel.drasniecia == 0:
            if cel.powazna_rana == 0:
                assert cel.powazna_rana == 0
            else:
                assert cel.powazna_rana == 1
        else:
            assert cel.drasniecia > 0
    else:
        assert cel.lekka_rana > 0


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
    return 10


def test_stalych():
    assert constants.mod(10) == 2
    assert constants.mod(5) == 0
    assert constants.KoscUmiejetnosci[1] > 2
    Bot.output("matematyka TG dziala bez zarzutu")
    return 3


def test_luskania_danych_z_excela():
    specki = excelDigger.Loader("Specjalizacje.xlsx", ["umiejetnasci"], ["B26"])
    specki = specki.zwroc()
    specki = specki[0]
    assert specki[1][0] == "bron boczna"
    Bot.output("ladowanie z excela dziala")
    return 2


def test_ran_kar_smierci(): #testy mortal.py
    wojtek = mortal.IstotaZywa(8, 8, 8, "Wojtek")
    wojtek.rana(10, 0)
    wojtek.rana(1)
    assert wojtek.rany[0] == 2
    assert wojtek.rany[1] == 1
    assert wojtek.rany[2] == 1
    Bot.output("podstawowy test Ran zakonczony")
    wojtek.redukcja_obrazen = 2
    wojtek.rana(3, 0)
    assert wojtek.rany[0] == 3
    assert wojtek.rany[1] == 1
    wojtek.rana(3, 0)
    wojtek.rana(3, 0)
    assert wojtek.rany[1] == 2
    Bot.output("test ran z redukcja obrazen zakonczony")
    wojtek.allokuj(5)
    assert wojtek.kara() == 11
    wojtek.allokuj(14)
    assert not wojtek.aktywacja(2)
    Bot.output("zaawansowany Bot aktywacji zakonczony")
    wojtek.allokuj(15)
    assert not wojtek.status
    return 9


def test_umiejetnosci_i_aktywacji(): # test mortal.py
    wojtek = mortal.IstotaZywa(8, 8, 8, "Wojtek")
    assert wojtek.aktywacja(2)
    assert wojtek.umiejetnasci[3][3] == 1
    assert wojtek.umiejetnasci[4][3] == 0
    assert wojtek.rzut_na_umiejetnasc("skupienie") >= 2
    Bot.output("umiejetnasci dzialaja")
    return 4


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
    return 15


def test_jezykow():
    wojtek = hero.Postac(8, 8, 8, ["bron boczna", "karabiny", "bron krotka"])
    wojtek.wykup_range("jezyki")
    assert wojtek.jezyki[0][1] == 3
    Bot.output("Jezyki dzialaja")
    return 1


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
    pisiontka = itemki.luskacz_amunicji("‘50 bmg")
    assert pisiontka[5] == "4d6"
    Bot.output("przedmioty dzialaja")
    return 6

"""
def test_dzialania_broni():
    wojtek = hero.Postac(8, 8, 8, ["bron boczna", "karabiny", "bron krotka"])
    cel = hero.Postac(8, 8, 8, ["bron boczna", "karabiny", "bron krotka"])
    giwera = items_old.Bron("strzelectwo", "2D2", 14, "m", 500)
    giwera.atakuj(wojtek, cel, 1)
    assert cel.rany[1] > 0
    giwera2 = items_old.Bron("strzelectwo", "2D2", -5, "ś", 0)
    assert giwera2.kosc_obrazen == "2D2"
    giwera2.atakuj(cel, wojtek, 2)
    assert wojtek.rany[1] == 0
    Bot.output("podstawowa Bron dziala")
"""


def test_dzialania_broni_strzeleckiej():
    itemki = items.Przedmioty('')
    m4ka = itemki.luskacz_broni("m4a1")
    M4KA = items.BronStrzelecka(m4ka)
    wojtek = hero.Postac(8, 8, 8, ["bron boczna", "karabiny", "bron krotka"])
    wojtek.aktywna_bron = M4KA
    beben = hero.Postac(8, 8, 8, ["bron boczna", "karabiny", "bron krotka"])
#    if wojtek.aktywna_bron.atakuj(wojtek, beben, 0):
#        sprawdz_jak_cel_oberwal(beben)
    assert M4KA.zasieg_minimalny == 0
    assert M4KA.zasieg_przyrost == 25
    Bot.output("TEN TEST BRONI STRZELECKIEJ JEST NEDOROBIONY, bo Bron palna ni chuja nie jest skonczona!")
    return 2

#do przerobki zalkowitej - inaczej  sie atakuje
def test_broni_bialej():
    itemki = items_old.Przedmioty('')
    noz = itemki.luskacz_broni_bialej("nóż")
    NOZ = items_old.BronBiala(noz)
    wojtek = hero.Postac(8, 8, 8, ["bron boczna", "karabiny", "bron krotka"])
    beben = hero.Postac(8, 8, 8, ["bron boczna", "karabiny", "bron krotka"])
    assert not NOZ.atakuj(wojtek, beben, 0)
    wojtek.wykup_range("walka wrecz")
    wojtek.wykup_range("walka wrecz")
    wojtek.wykup_range("walka wrecz")
    wojtek.wykup_range("walka wrecz")
    wojtek.wykup_range("walka wrecz")
    wojtek.wykup_range("walka wrecz")
    assert NOZ.atakuj(wojtek, beben, 0)
    return 2

def test_amunicji_i_magazynkow():
    itemki = items.Przedmioty('')
    natowska = itemki.luskacz_amunicji("5,56 nato")
    NATO = items.Amunicja(natowska)
    m4ka = itemki.luskacz_broni("m4a1")
    M4KA = items.BronStrzelecka(m4ka)
    scout = itemki.luskacz_broni("steyr scout")
    scout = items.BronStrzelecka(scout)
    mag = items.Magazynek(M4KA)
    mag.zaladuj_magazynek(NATO)
    mag_scout = items.Magazynek(scout)
    assert NATO.ilosc_amunicji == 45
    assert mag.stan_nabojow == 30
    mag_scout.zaladuj_magazynek(NATO)
    assert NATO.ilosc_amunicji == 35
    assert mag_scout.stan_nabojow == 10
    scout.zmien_magazynek(mag_scout)
    scout.zaciagnij_naboj()
    assert scout.naboj_w_komorze
    M4KA.zmien_magazynek(mag)
    assert not M4KA.naboj_w_komorze
    M4KA.zaciagnij_naboj()
    assert M4KA.aktualny_magazynek.stan_nabojow == 29
    assert M4KA.naboj_w_komorze
    return 8


#trzeba go dorobic
def test_mechanik_walki():
    Bot.output("test samej walki")
    itemki = items.Przedmioty('')
    natowska = itemki.luskacz_amunicji("5,56 nato")
    NATO = items.Amunicja(natowska)
    m4ka = itemki.luskacz_broni("m4a1")
    M4KA = items.BronStrzelecka(m4ka)
    mag = items.Magazynek(M4KA)
    mag.zaladuj_magazynek(NATO)
    M4KA.zmien_magazynek(mag)
    M4KA.zaciagnij_naboj()
    strzelanie = mechanics.Shooting()
    wojtek = hero.Postac(8, 8, 8, ["bron boczna", "karabiny", "bron krotka"])
    wojtek.aktywna_bron = M4KA
    beben = hero.Postac(8, 8, 8, ["bron boczna", "karabiny", "bron krotka"])
    x = strzelanie.strzelaj(wojtek, beben, 50, "pojedynczy")
    wojtek.wykup_range("strzelectwo")
    wojtek.wykup_range("strzelectwo")
    wojtek.wykup_range("strzelectwo")
    wojtek.wykup_range("strzelectwo")
    wojtek.wykup_range("strzelectwo")
    x = x + strzelanie.strzelaj(wojtek, beben, 50, "serie")
    x = x + strzelanie.strzelaj(wojtek, beben, 50, "samoczynny")
    x = x + strzelanie.strzelaj(wojtek, beben, 50, "pojedynczy")
    assert wojtek.aktywna_bron.aktualny_magazynek.stan_nabojow == 12
    scout = itemki.luskacz_broni("steyr scout")
    scout = items.BronStrzelecka(scout)
    mag_scout = items.Magazynek(scout)
    mag_scout.zaladuj_magazynek(NATO)
    scout.zmien_magazynek(mag_scout)
    wojtek.aktywna_bron = scout
    assert not strzelanie.strzelaj(wojtek, beben, 50, "serie")
    wojtek.aktywna_bron.zaciagnij_naboj()
    assert strzelanie.strzelaj(wojtek, beben, 50, "serie")
    print(wojtek.aktywna_bron.naboj_w_komorze)
    assert not strzelanie.strzelaj(wojtek, beben, 50, "serie")
    wojtek.aktywna_bron.zaciagnij_naboj()
    assert strzelanie.strzelaj(wojtek, beben, 50, "samoczynny")
    assert wojtek.aktywna_bron.aktualny_magazynek.stan_nabojow == 8
    return 8

ilosc_testow_pass = 0
ilosc_testow_pass = test_luskania_danych_z_excela()
ilosc_testow_pass += test_systemu()
ilosc_testow_pass += test_stalych()
ilosc_testow_pass += test_ran_kar_smierci()
ilosc_testow_pass += test_umiejetnosci_i_aktywacji()
ilosc_testow_pass += test_wykupowania_umiejetnosci_z_obnizeniem_przez_specjalizacje()
ilosc_testow_pass += test_jezykow()
ilosc_testow_pass += test_przedmiotow()
#test_dzialania_broni()
ilosc_testow_pass += test_dzialania_broni_strzeleckiej()
ilosc_testow_pass += test_broni_bialej()
ilosc_testow_pass += test_mechanik_walki()
ilosc_testow_pass += test_amunicji_i_magazynkow()
print("przeszlo " + str(ilosc_testow_pass) + " testow \nJest to " + str(ilosc_testow_pass/70 * 100) + "% testów.")
#unittest.main()
