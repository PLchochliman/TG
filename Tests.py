import mortal_base as mortal
import constans as constants
import Bot as Bot
import excelDigger as excelDigger
import mortal_hero as hero
import przedmioty_bron as items
import mechanics as mechanics
import items_read_from_excel as raw_items
import items_read_from_SQL as SQL
import przedmioty_ochronne as przedmioty_ochronne

#  przedmioty_jako_rekord = raw_items.Przedmioty()
przedmioty_jako_rekord = SQL.Przedmioty(False)  # change to True to update base

def sprawdz_czy_cel_oberwal(cel):
    for rana in cel.rany:
        if not isinstance(rana, list):
            if rana > 0:
                return 1



def wez_i_zaladuj_giwere(nazwa_giwery):
    nazwa_giwery = nazwa_giwery.lower()
    giwera = przedmioty_jako_rekord.luskacz_broni(nazwa_giwery)
    giwera = items.BronStrzelecka(giwera)
    mag = items.Magazynek(giwera)
    ammo = przedmioty_jako_rekord.luskacz_amunicji(giwera.statystyki_podstawowe[8])
    ammo = items.Amunicja(ammo)
    mag.zaladuj_magazynek(ammo)
    giwera.zmien_magazynek(mag)
    giwera.zaciagnij_naboj()
    giwera.zloz_sie_do_strzalu()
    return giwera


def dokup_i_zaladuj_magazynek(giwera):
    mag = items.Magazynek(giwera)
    ammo = przedmioty_jako_rekord.luskacz_amunicji(giwera.statystyki_podstawowe[8])
    ammo = items.Amunicja(ammo)
    mag.zaladuj_magazynek(ammo)
    return mag


def wez_i_zmien_celownik(giwera, nazwa_celownika):
    return giwera.zmien_celownik(items.Celownik(przedmioty_jako_rekord.luskacz_celownikow(nazwa_celownika)))


def postac_co_z_pistoletu_i_karabinu_rzuca_6():
    wojtek = hero.Postac(8, 8, 8, ["bron boczna", "karabiny", "bron krotka"])
    wojtek.podnies_umiejetnosc_specjalizacji("bron boczna", "wprawa")
    wojtek.podnies_umiejetnosc_specjalizacji("bron boczna", "wprawa")
    wojtek.podnies_umiejetnosc_specjalizacji("bron boczna", "wprawa")
    wojtek.podnies_umiejetnosc_specjalizacji("bron boczna", "wprawa")
    wojtek.podnies_umiejetnosc_specjalizacji("bron boczna", "wprawa")
    wojtek.podnies_umiejetnosc_specjalizacji("bron boczna", "wprawa")
    wojtek.podnies_umiejetnosc_specjalizacji("karabiny", "wprawa")
    wojtek.podnies_umiejetnosc_specjalizacji("karabiny", "wprawa")
    wojtek.podnies_umiejetnosc_specjalizacji("karabiny", "wprawa")
    wojtek.podnies_umiejetnosc_specjalizacji("karabiny", "wprawa")
    wojtek.podnies_umiejetnosc_specjalizacji("karabiny", "wprawa")
    wojtek.podnies_umiejetnosc_specjalizacji("karabiny", "wprawa")
    return wojtek


def gong_o_uniku_10():
    return hero.Postac(8, 7, 7, ["bron boczna", "karabiny", "bron krotka"], "gong")


def test_runner(test):
    def parser():
        try:
            return test()
        except AssertionError as inst:
            print(type(inst))
            print(inst.args)
#            print(str(inst.with_traceback()))
            print(test.__name__)
            return 0
    return parser


@test_runner
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


@test_runner
def test_stalych():
    assert constants.mod(10) == 2
    assert constants.mod(5) == 0
    assert constants.KoscUmiejetnosci[1] > 2
    Bot.output("matematyka TG dziala bez zarzutu")
    return 3


@test_runner
def test_luskania_danych_z_excela():
    specki = excelDigger.Loader("Specjalizacje.xlsx", ["umiejetnasci"], ["B26"])
    specki = specki.zwroc()
    specki = specki[0]
    assert specki[1][0] == "bron boczna"
    Bot.output("ladowanie z excela dziala")
    return 2


@test_runner
def test_ran_kar_smierci(): #testy mortal_base.py
    wojtek = mortal.IstotaZywa(8, 8, 8, "Wojtek")
    assert wojtek.w_ruchu == 0
    wojtek.zaplanuj_akcje("krok")
    wojtek.akcja()
    assert wojtek.w_ruchu == -1
    wojtek.zaplanuj_akcje("chód")
    wojtek.akcja()
    assert wojtek.w_ruchu == -5
    wojtek.zaplanuj_akcje("bieg")
    wojtek.akcja()
    assert wojtek.w_ruchu == -10
    wojtek.zaplanuj_akcje("kurwa sram")
    wojtek.akcja()
    assert wojtek.w_ruchu == 0
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
    return 15


@test_runner
def test_uniku(): #testy mortal_base.py
    wojtek = mortal.IstotaZywa(8, 8, 8, "Wojtek")
    assert wojtek.aktualny_unik() == 12
    assert wojtek.zmien_oslone(2) == 2
    assert wojtek.oslona == 2
    assert wojtek.aktualny_unik() == 14
    assert wojtek.zmien_oslone(12) == 0
    assert wojtek.aktualny_unik() == 12
    return 7


@test_runner
def test_umiejetnosci_i_aktywacji(): # test mortal_base.py
    wojtek = mortal.IstotaZywa(8, 8, 8, "Wojtek")
    assert wojtek.aktywacja(2)
    assert wojtek.umiejetnosci[3][3] == 1
    assert wojtek.umiejetnosci[4][3] == 0
    assert wojtek.rzut_na_umiejetnasc("skupienie") >= 2
    Bot.output("umiejetnosci dzialaja")
    return 4


@test_runner
def test_wykupowania_umiejetnosci_z_obnizeniem_przez_specjalizacje_oraz_umiejetnosci_specjalizacji():
    wojtek = hero.Postac(8, 8, 8, ["bron boczna", "karabiny", "bron krotka"])
    wojtek.wykup_range("obsluga broni")
    assert wojtek.punktyUmiejetnasci == 165
    assert wojtek.umiejetnosci[1][0] == 1
    wojtek.wykup_range("obsluga broni")
    assert wojtek.punktyUmiejetnasci == 164
    assert wojtek.umiejetnosci[1][0] == 2
    wojtek.wykup_range("gadana")
    assert wojtek.punktyUmiejetnasci == 161
    assert wojtek.umiejetnosci[15][0] == 1
    wojtek.wykup_range("prowadzenie pojazdu")
    assert wojtek.punktyUmiejetnasci == 159
    assert wojtek.umiejetnosci[8][0] == 1
    wojtek.wykup_range("gadana")
    assert wojtek.punktyUmiejetnasci == 153
    assert wojtek.umiejetnosci[15][0] == 2
    wojtek.wykup_range("prowadzenie pojazdu")
    assert wojtek.punktyUmiejetnasci == 149
    assert wojtek.umiejetnosci[8][0] == 2
    assert wojtek.rzut_na_umiejetnasc("prowadzenie pojazdu") > 3
    wojtek.podnies_predyspozycje("bron boczna")
    assert wojtek.umiejetnosci[8][3] == 2
    wojtek.wykup_range("zmysl bitewny")
    assert wojtek.unik == 13
    Bot.output("wykupowanie umiejetnosci dziala")
    wojtek.podnies_umiejetnosc_specjalizacji("bron boczna", "wprawa")
    assert wojtek.punktyUmiejetnasci == 146
    assert wojtek.specjalizacje[0][2] == 1
    wojtek.podnies_umiejetnosc_specjalizacji("bron boczna", "wprawa")
    wojtek.podnies_umiejetnosc_specjalizacji("bron boczna", "wprawa")
    wojtek.podnies_umiejetnosc_specjalizacji("bron boczna", "wprawa")
    wojtek.podnies_umiejetnosc_specjalizacji("bron boczna", "wprawa")
    wojtek.podnies_umiejetnosc_specjalizacji("bron boczna", "wprawa")
    assert wojtek.punktyUmiejetnasci == 106
    return 16


@test_runner
def test_jezykow():
    wojtek = hero.Postac(8, 8, 8, ["bron boczna", "karabiny", "bron krotka"])
    wojtek.wykup_range("jezyki")
    assert wojtek.jezyki[0][1] == 3
    Bot.output("Jezyki dzialaja")
    return 1


@test_runner
def test_przedmiotow():
    m4ka = przedmioty_jako_rekord.luskacz_broni("m4a1")
    assert m4ka[6] == 'ś'
    nozyk = przedmioty_jako_rekord.luskacz_broni_bialej("nóż")
    assert nozyk[3] == 3
    hek = przedmioty_jako_rekord.luskacz_granatow("granat ofensywny")
    assert hek[2] == "2d6"
    acog = przedmioty_jako_rekord.luskacz_celownikow("acogx4")
    assert acog[3] == 10
    trijcon = przedmioty_jako_rekord.luskacz_celownikow("trijcon")
    assert trijcon[4] == "strzelby"
    pisiontka = przedmioty_jako_rekord.luskacz_amunicji("‘50 bmg")
    assert pisiontka[5] == "4d6"
    Bot.output("przedmioty dzialaja")
    return 6


@test_runner
def test_Broni_strzelcekiej_magazynki_zaciaganie_amunicja_czterotakt():
    m4ka = przedmioty_jako_rekord.luskacz_broni("m4a1")
    M4KA = items.BronStrzelecka(m4ka)
    wojtek = hero.Postac(8, 8, 8, ["bron boczna", "karabiny", "bron krotka"])
    wojtek.aktywna_bron = M4KA
    assert M4KA.zasieg_minimalny == 0
    assert M4KA.zasieg_przyrost == 25
    print(M4KA.szybkostrzelnosc)
    assert M4KA.szybkostrzelnosc == 13
    assert M4KA.zasieg_minimalny == 0
    assert M4KA.penetracja == 3
    assert M4KA.zasieg_maksymalny == 300
    assert M4KA.aktualny_magazynek.stan_nabojow == 0
    assert M4KA.aktualny_magazynek.maksymalna_pojemnosc == 30
    natowska = przedmioty_jako_rekord.luskacz_amunicji("5,56 nato")
    NATO = items.Amunicja(natowska)
    ak = przedmioty_jako_rekord.luskacz_amunicji("5,45 x 39")
    ak = items.Amunicja(ak)
    assert M4KA.aktualny_magazynek.zaladuj_magazynek(NATO)
    assert not M4KA.aktualny_magazynek.wyladuj_amunicje(ak)
    assert M4KA.aktualny_magazynek.wyladuj_amunicje(NATO)
    assert NATO.ilosc_amunicji == 75
    assert not M4KA.zaciagnij_naboj()
    mosin = przedmioty_jako_rekord.luskacz_broni("mosin nagant")
    mosin = items.BronStrzelecka(mosin)
    wojtek.aktywna_bron = mosin
    radziecka = przedmioty_jako_rekord.luskacz_amunicji("7,62 x 54 r")
    czerwona = items.Amunicja(radziecka)
    stal = items.Magazynek(mosin)
    stal.zaladuj_magazynek(czerwona)
    #TODO coś nie tak z amunicją i jej zaciąganiem
    assert wojtek.aktywna_bron.zmien_magazynek(stal)
    assert wojtek.aktywna_bron.zaciagnij_naboj()
    mag = items.Magazynek(mosin)
    mag.zaladuj_magazynek(czerwona)
    assert wojtek.aktywna_bron.zmien_magazynek(mag)
    saw = przedmioty_jako_rekord.luskacz_broni("m249 saw")
    SAW = items.BronStrzelecka(saw)
    stal = items.Magazynek(SAW)
    stal.zaladuj_magazynek(NATO)
    mag = items.Magazynek(M4KA)
    mag.zaladuj_magazynek(NATO)
    assert SAW.zmien_magazynek(mag)
    assert SAW.zmien_magazynek(stal)
    assert SAW.zaciagnij_naboj()
    assert SAW.kara_za_nierostawienie == -4
    natowska = przedmioty_jako_rekord.luskacz_amunicji("7,62 nato")
    NATO = items.Amunicja(natowska)
    swina = przedmioty_jako_rekord.luskacz_broni("m240b")
    Swinia = items.BronStrzelecka(swina)
    stal = items.Magazynek(Swinia)
    stal.zaladuj_magazynek(NATO)
    assert Swinia.zmien_magazynek(stal)
    assert Swinia.zaciagnij_naboj()
    assert Swinia.kara_za_nierostawienie == -10
    assert Swinia.rostaw_bron() == 0
    return 24


@test_runner
def test_broni_strzeleckiej_specjalne_magi():
    mk23 = przedmioty_jako_rekord.luskacz_broni("mk23")
    MK23 = items.BronStrzelecka(mk23)
    wojtek = hero.Postac(8, 8, 8, ["bron boczna", "karabiny", "bron krotka"])
    wojtek.aktywna_bron = MK23
    ACP = przedmioty_jako_rekord.luskacz_amunicji("acp'45")
    ACP = items.Amunicja(ACP)
    mag = items.Magazynek(MK23)
    mag.zaladuj_magazynek(ACP)
    powiekszaony_mag = items.Magazynek(MK23, "powiekszone magazynki")
    powiekszaony_mag.zaladuj_magazynek(ACP)
    assert powiekszaony_mag.stan_nabojow == 18

    return 1


@test_runner
def test_broni_strzeleckiej_z_Celownikami():
    giwera = wez_i_zaladuj_giwere("AKM")
    assert not wez_i_zmien_celownik(giwera, "aimpoint")
    return 1

@test_runner
def test_broni_bialej():
    ww = mechanics.WalkaWrecz()
    wojtek = hero.Postac(8, 8, 8, ["bron boczna", "karabiny", "bron krotka"], "operejtor")
    noz = przedmioty_jako_rekord.luskacz_broni_bialej("nóż")
    piesc = przedmioty_jako_rekord.luskacz_broni_bialej("kolba")
    NOZ = items.BronBiala(noz)
    obrywa = hero.Postac(5, 5, 5, ["bron boczna", "karabiny", "bron krotka"], "obrywacz")
    assert not ww.uderz(wojtek, obrywa, 0)
    assert not ww.uderz(wojtek, obrywa, 1)
    wojtek.wykup_range("walka wrecz")
    wojtek.wykup_range("walka wrecz")
    wojtek.wykup_range("walka wrecz")
    wojtek.wykup_range("walka wrecz")
    wojtek.wykup_range("walka wrecz")
    wojtek.wykup_range("walka wrecz")
    assert ww.uderz(wojtek, obrywa, 0)
    wojtek.aktywna_bron = NOZ
    assert ww.uderz(wojtek, obrywa, 0)
    m4ka = przedmioty_jako_rekord.luskacz_broni("m4a1")
    M4KA = items.BronStrzelecka(m4ka)
    wojtek.aktywna_bron = M4KA
    assert ww.uderz(wojtek, obrywa, 0)
    return 5


@test_runner
def test_amunicji_i_magazynkow():
    natowska = przedmioty_jako_rekord.luskacz_amunicji("5,56 nato")
    NATO = items.Amunicja(natowska)
    m4ka = przedmioty_jako_rekord.luskacz_broni("m4a1")
    M4KA = items.BronStrzelecka(m4ka)
    scout = przedmioty_jako_rekord.luskacz_broni("steyr scout")
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
    srut = przedmioty_jako_rekord.luskacz_amunicji("12g")
    Srut = items.Amunicja(srut)
    mcs = przedmioty_jako_rekord.luskacz_broni("870 mcs")
    MCS = items.BronStrzelecka(mcs)
    rura = items.Magazynek(MCS)
    rura.zaladuj_magazynek(Srut)
    assert not MCS.zmien_magazynek(rura)
    assert MCS.aktualny_magazynek.zaladuj_magazynek(Srut)
    assert MCS.zaciagnij_naboj()
    srut = przedmioty_jako_rekord.luskacz_amunicji("12g")
    breneka = items.Amunicja(srut, 1, "breneka")
    assert breneka.nazwa_amunicji == "12g breneka"
    natowska = przedmioty_jako_rekord.luskacz_amunicji("5,56 nato")
    NATO = items.Amunicja(natowska, 1, "przeciwpancerna")
    assert NATO.nazwa_amunicji == "5,56 nato przeciwpancerna"
    assert NATO.penetracja == 4
    assert NATO.kosc_obrazen == "d6"
    dziewiatka = przedmioty_jako_rekord.luskacz_amunicji("9mm parabellum")
    dziewiatka = items.Amunicja(dziewiatka, 1, "przeciwpancerna")
    assert dziewiatka.penetracja == 2
    assert dziewiatka.kosc_obrazen == "d4"
    siodemka = przedmioty_jako_rekord.luskacz_amunicji("7,62 nato")
    Siodemka = items.Amunicja(siodemka, 1, "przeciwpancerna")
    assert Siodemka.penetracja == 4
    assert Siodemka.kosc_obrazen == "d8"
    dziewiatka = przedmioty_jako_rekord.luskacz_amunicji("9mm parabellum")
    dziewiatka = items.Amunicja(dziewiatka, 1, "9mm++")
    assert dziewiatka.odrzut == -4
    assert dziewiatka.penetracja == 2
    ACP = przedmioty_jako_rekord.luskacz_amunicji("acp'45")
    ACP = items.Amunicja(ACP)
    assert ACP.odrzut == -2
    assert ACP.specjalne == ["wytłumiona"]
    return 23


@test_runner
def test_mechanik_walki():
    Bot.output("test samej walki")
    natowska = przedmioty_jako_rekord.luskacz_amunicji("5,56 nato")
    NATO = items.Amunicja(natowska)
    m4ka = przedmioty_jako_rekord.luskacz_broni("m4a1")
    M4KA = items.BronStrzelecka(m4ka)
    mag = items.Magazynek(M4KA)
    mag.zaladuj_magazynek(NATO)
    M4KA.zmien_magazynek(mag)
    M4KA.zaciagnij_naboj()
    strzelanie = mechanics.Strzelanie()
    wojtek = hero.Postac(8, 8, 8, ["bron boczna", "karabiny", "bron krotka"])
    wojtek.aktywna_bron = M4KA
    beben = hero.Postac(2, 2, 2, ["bron boczna", "karabiny", "bron krotka"])
    x = strzelanie.strzal(wojtek, beben, 50, "pojedynczy")
    wojtek.wykup_range("strzelectwo")
    wojtek.wykup_range("strzelectwo")
    wojtek.wykup_range("strzelectwo")
    wojtek.wykup_range("strzelectwo")
    wojtek.wykup_range("strzelectwo")
    x = x + strzelanie.strzal(wojtek, beben, 50, "serie")
    x = x + strzelanie.strzal(wojtek, beben, 50, "samoczynny")
    x = x + strzelanie.strzal(wojtek, beben, 50)
    print(wojtek.aktywna_bron.aktualny_magazynek.stan_nabojow)
    assert wojtek.aktywna_bron.aktualny_magazynek.stan_nabojow == 11
    scout = wez_i_zaladuj_giwere("steyr scout")
    scout.naboj_w_komorze = False
    wojtek.aktywna_bron = scout
    assert not strzelanie.strzal(wojtek, beben, 15, "serie")
    wojtek.aktywna_bron.zloz_sie_do_strzalu()
    assert wojtek.aktywna_bron.zaciagnij_naboj()
    assert strzelanie.strzal(wojtek, beben, 15, "serie")
    wojtek.aktywna_bron.zaciagnij_naboj()
    assert strzelanie.strzal(wojtek, beben, 15, "samoczynny")
    assert wojtek.aktywna_bron.aktualny_magazynek.stan_nabojow == 7
    wojtek.aktywna_bron.zaciagnij_naboj()
    assert wojtek.aktywna_bron.aktualny_magazynek.stan_nabojow == 6
    wojtek.aktywna_bron.awaria = True
    assert not strzelanie.strzal(wojtek, beben, 50, "serie")
    return 10



@test_runner
def test_zasad_specjalnych_i_dodatkow_do_broni():
    wojtek = postac_co_z_pistoletu_i_karabinu_rzuca_6()
    wojtek.aktywna_bron = wez_i_zaladuj_giwere("AKM")
    wojtek.aktywna_bron.dokup_szyny(wojtek)
    assert wez_i_zmien_celownik(wojtek.aktywna_bron, "aimpoint")
    gong = gong_o_uniku_10()
    strzelanie = mechanics.Strzelanie()
    wojtek.aktywna_bron.rostaw_bron()
    assert strzelanie.strzal(wojtek, gong, 5)   #sprawdzona wprawa i podstawowe liczenie z AK
    assert strzelanie.strzal(wojtek, gong, 5)
    wojtek.aktywna_bron = wez_i_zaladuj_giwere("SR25")
    assert wojtek.aktywna_bron.zamontuj_dodatek(items.DodatekDoBroni(przedmioty_jako_rekord.luskacz_dodatkow("dwójnóg")))
    assert not strzelanie.strzal(wojtek, gong, 5)
    assert wojtek.aktywna_bron.szyny_montazowe[1].aktywacja()
    assert strzelanie.strzal(wojtek, gong, 5)
    assert wojtek.aktywna_bron.szyny_montazowe[1].nazwa == "dwójnóg"
    assert wojtek.aktywna_bron.szyny_montazowe[1].zdejmij(wojtek.aktywna_bron)
    wojtek.aktywna_bron = wez_i_zaladuj_giwere("fiveseven")
    assert wojtek.aktywna_bron.zamontuj_dodatek(items.DodatekDoBroni(przedmioty_jako_rekord.luskacz_dodatkow("laser")))
    assert wojtek.aktywna_bron.szyny_montazowe[0] == "nie"
    assert not strzelanie.strzal(wojtek, gong, 5)
    assert wojtek.aktywna_bron.szyny_montazowe[1].aktywacja()
    assert not strzelanie.strzal(wojtek, gong, 5)
    assert wojtek.aktywna_bron.zamontuj_dodatek(items.Celownik(przedmioty_jako_rekord.luskacz_celownikow("perfekcyjne")))
    assert not strzelanie.strzal(wojtek, gong, 5)
    assert wojtek.aktywna_bron.zamontuj_dodatek(items.Celownik(przedmioty_jako_rekord.luskacz_celownikow("micro")))
    assert strzelanie.strzal(wojtek, gong, 5)
    return 19


@test_runner
def test_szpeju():
    rekord = przedmioty_jako_rekord.wyszukaj_przedmiot_i_zwroc_po_wszystkim("plate carrier")
    kamza = przedmioty_ochronne.ElementSzpeju(rekord)
    wojtek = postac_co_z_pistoletu_i_karabinu_rzuca_6()
    assert kamza.zaloz(wojtek)
    assert wojtek.element_szpeju[constants.miejsce_na_ciele["klata"]].nazwa == "plate carrier"
    rekord = przedmioty_jako_rekord.wyszukaj_przedmiot_i_zwroc_po_wszystkim("skarab")
    kamza = przedmioty_ochronne.ElementSzpeju(rekord)
    assert not kamza.zaloz(wojtek)
    assert wojtek.element_szpeju[constants.miejsce_na_ciele["klata"]].zdejmij(wojtek)
    assert kamza.zaloz(wojtek)
    assert wojtek.element_szpeju[constants.miejsce_na_ciele["pas"]].nazwa == "skarab"
    assert wojtek.element_szpeju[constants.miejsce_na_ciele["klata"]].maksymakny_unik == 15
    rekord = przedmioty_jako_rekord.wyszukaj_przedmiot_i_zwroc_po_wszystkim("klasa 3 miękkie")
    assert wojtek.pieniadze == 9000
    assert wojtek.element_szpeju[constants.miejsce_na_ciele["klata"]].kup_i_wloz_plyte_do_kamizelki(wojtek, rekord)
    assert wojtek.pieniadze == 8450
    wojtek.aktywna_bron = wez_i_zaladuj_giwere("SCAR-L")
    mag = dokup_i_zaladuj_magazynek(wojtek.aktywna_bron)
    assert wojtek.element_szpeju[constants.miejsce_na_ciele["klata"]].schowaj_przedmiot(mag)
    assert wojtek.aktywna_bron.zmien_magazynek(wojtek.element_szpeju[constants.miejsce_na_ciele["klata"]]
                                               .wyciagnij_magazynek(wojtek.aktywna_bron))

    mag = dokup_i_zaladuj_magazynek(wojtek.aktywna_bron)
    assert wojtek.element_szpeju[constants.miejsce_na_ciele["klata"]].schowaj_przedmiot(mag)
    wojtek.aktywna_bron = wez_i_zaladuj_giwere("M4A1")
    assert wojtek.aktywna_bron.zmien_magazynek(wojtek.element_szpeju[constants.miejsce_na_ciele["klata"]]
                                               .wyciagnij_magazynek(wojtek.aktywna_bron))
    return 14


@test_runner
def test_obrywania_w_kamze_i_mundurze():
    strzelanie = mechanics.Strzelanie()
    rekord = przedmioty_jako_rekord.wyszukaj_przedmiot_i_zwroc_po_wszystkim("plate carrier")
    kamza = przedmioty_ochronne.ElementSzpeju(rekord)
    wojtek = postac_co_z_pistoletu_i_karabinu_rzuca_6()
    gong = gong_o_uniku_10()
    kamza.zaloz(gong)
    wojtek.aktywna_bron = wez_i_zaladuj_giwere("MP5A3")
    rekord = przedmioty_jako_rekord.wyszukaj_przedmiot_i_zwroc_po_wszystkim("klasa 3 miękkie")
    assert gong.element_szpeju[constants.miejsce_na_ciele["klata"]].kup_i_wloz_plyte_do_kamizelki(gong, rekord)
    assert strzelanie.strzal(wojtek, gong, 10)
    assert not sprawdz_czy_cel_oberwal(gong)
    wojtek.aktywna_bron = wez_i_zaladuj_giwere("SCAR-L")
    assert not strzelanie.strzal(wojtek, gong, 10)
    wez_i_zmien_celownik(wojtek.aktywna_bron, "aimpoint")
    assert strzelanie.strzal(wojtek, gong, 10)
    assert sprawdz_czy_cel_oberwal(gong)
    rekord = przedmioty_jako_rekord.wyszukaj_przedmiot_i_zwroc_po_wszystkim("kontraktowy")
    gong.element_szpeju[constants.miejsce_na_ciele["mundur"]] = przedmioty_ochronne.Ubranie(rekord)
    assert not strzelanie.strzal(wojtek, gong, 10)
    return 7



@test_runner
def test_akcji():
    akcja = mechanics.Akcje()
    assert akcja.przesun_faze(15)
    assert akcja.tura == 2
    assert akcja.faza == 3
    return 3


#citizien for, film o Snowdenie
ilosc_testow_pass = 0
ilosc_testow_pass = test_luskania_danych_z_excela()
ilosc_testow_pass += test_systemu()
ilosc_testow_pass += test_stalych()
ilosc_testow_pass += test_uniku()
ilosc_testow_pass += test_ran_kar_smierci()
ilosc_testow_pass += test_umiejetnosci_i_aktywacji()
ilosc_testow_pass += test_wykupowania_umiejetnosci_z_obnizeniem_przez_specjalizacje_oraz_umiejetnosci_specjalizacji()
ilosc_testow_pass += test_jezykow()
ilosc_testow_pass += test_przedmiotow()
ilosc_testow_pass += test_Broni_strzelcekiej_magazynki_zaciaganie_amunicja_czterotakt()
ilosc_testow_pass += test_broni_bialej()
ilosc_testow_pass += test_mechanik_walki()
ilosc_testow_pass += test_amunicji_i_magazynkow()
ilosc_testow_pass += test_akcji()
ilosc_testow_pass += test_broni_strzeleckiej_specjalne_magi()
ilosc_testow_pass += test_broni_strzeleckiej_z_Celownikami()
ilosc_testow_pass += test_zasad_specjalnych_i_dodatkow_do_broni()
ilosc_testow_pass += test_szpeju()
ilosc_testow_pass += test_obrywania_w_kamze_i_mundurze()

print("Z wynikiem pozytywynym przeszło " + str(ilosc_testow_pass) + " testow \n"
      "Jest to " + str(ilosc_testow_pass/171 * 100) + "% testów.")
#unittest.main()

