
import Bot as Bot
import constans as constants


class Przedmiot():
    wartosc = 0
    waga = 0
    nazwa = ""

    def __init__(self, wartosc, masa):
        self.wartosc = wartosc
        self.masa = masa
        self.nazwa = ""

    def zwroc_mase(self):
        return self.masa

    def zwroc_wartosc(self):
        return self.wartosc



class DodatekDoBroni(Przedmiot):
    premia = 0
    efekt = ""
    aktywowany = False
    aktywny = False
    wymaga_zlozenia = False
    masa = 0
    cena = 1
    specjalne = ""

    def __init__(self, czysta_dana):
        self.nazwa = czysta_dana[0]
        self.efekt = czysta_dana[1]
        self.premia = czysta_dana[2]
        if "tak" in czysta_dana[3]:
            self.aktywowany = True
            self.aktywny = False
        else:
            self.aktywowany = False
            self.aktywny = True
        if czysta_dana[4] == "tak":
            self.wymaga_zlozenia = True
        else:
            self.wymaga_zlozenia = False
        self.specjalne = czysta_dana[5]
        self.masa = czysta_dana[6]
        self.cena = czysta_dana[7]

    def zaloz(self, bron):
        miejsce = self
        return True

    def zdejmij(self, bron):
        miejsce = []
        return True

    def dzialanie(self, bron, akcja):
        return 0


class Celownik(DodatekDoBroni):
    przyrost_zasiegu = 0
    zasady_specjalne = ""
    typ = ""
    czas_do_zlozenia = 0
    zasieg_minimalny = 0

    def __init__(self, czysta_dana):
        self.nazwa = czysta_dana[0]
        self.wartosc = czysta_dana[-1]
        self.masa = czysta_dana[-2]
        self.premia = czysta_dana[1]
        self.przyrost_zasiegu = czysta_dana[2]
        if czysta_dana[3] in ['', '-']:
            self.zasieg_minimalny = 0
        else:
            self.zasieg_minimalny = int(czysta_dana[3])
        self.zasady_specjalne = czysta_dana[4]
        self.typ = czysta_dana[5]
        self.czas_do_zlozenia = czysta_dana[6]


    def zaloz(self, bron):
        if self.typ == "mechaniczne":
            bron.celownik = self
            return True
        if bron.szyny_montazowe[0] == "tak":
            bron.celownik = self
            bron.szyny_montazowe[0] = self
            return True

        if "pistolet" in bron.zasady_specjalne:
            if "pistolety" in self.zasady_specjalne:
                bron.celownik = self
                return True
        Bot.output("Nie masz odpowiedniej szyny/ jest zajęta")
        return False

    def zdejmij(self, bron):
        bron.celownik = Celownik(('zwykłe', 0, 25, '', 'w nocy kara -4,', 2, 0, '-'))
        if self.typ == "mechaniczne":
            return True
        if "pistolety" in self.zasady_specjalne:
            return True
        bron.szyny_montazowe[0] = "tak"
        return True

"""
it's all about the ammunition for the gun.
"""

class Amunicja:
    nazwa_naboju = ""
    kosc_obrazen = ""
    typ_amunicji = ""
    penetracja = 0
    odrzut = 0
    nazwa_amunicji = ""
    ilosc_paczek = 0
    ilosc_amunicji: int = 0
    cena = 0
    maks_zasieg_amunicji = 0
    charakterystyka_naboju = ""
    specjalne = []

    def __init__(self, amunicja, ilosc_paczek=1, typ_amunicji="podstawowa"):
        self.odrzut = amunicja[4]
        self.nazwa_naboju = amunicja[0]
        self.kosc_obrazen = amunicja[5]
        self.penetracja = constants.penetracja[amunicja[6]]
        self.typ_amunicji = typ_amunicji
        self.nazwa_amunicji = self.nazwa_naboju + " " + self.typ_amunicji
        self.ilosc_amunicji = ilosc_paczek * amunicja[2]
        self.ilosc_paczek = ilosc_paczek
        self.cena = amunicja[3]
        self.maks_zasieg_amunicji = amunicja[8]
        self.charakterystyka_naboju = amunicja[1]
        self.specjalne = amunicja[7].split(",")
        self.__dostosuj_specjalna_amunicje()

    """
    zadawanie obrażenia
    Gumowe kule do implementacji
    Kość obrażeń zmniejszona o połowę, po zadaniu Out of action, nie staje się Out of Action a Obezwładniony. 
    Po 30 minutach wstaje i regeneruje wszystkie rany z kulowych kul jakby nigdy nic. Po zadaniu lekkiej, rzuć na 
    obezwładnienie. rzuć na D6. Jeśli rzut jest równy/wyższy 6, obezwładnia. Jeżeli ma poważną ranę, i zadasz mu lekką
     ranę, obezwładnia natychmiastowo. Nie ma penetracji. Domyślnie poddźwiękowa. Zasięg skuteczny to 50m. nie do 
     połączona z czymkolwiek, nawet jeśli zasady drugiej amunicji mówi co innego..
    """
    def zadaj_obrazenia(self, cel, premia, zasieg):
        # TODO może przerobić na zwrot do broni i egzekucję obrażeń w broni?
        if self.typ_amunicji == "grzybkująca":
            cel.rana(self.rzut_na_obrazenia(0) + premia, self.penetracja)
            cel.rana(self.rzut_na_obrazenia("d6") + premia, self.penetracja)
            return True
        if self.typ_amunicji == "wyborowe":
            premia = premia * 4
        cel.rana(self.rzut_na_obrazenia(0) + premia, self.penetracja)
        return True
    #obrazenia=kosc_obrazen
    def rzut_na_obrazenia(self, obrazenia):
        if obrazenia == 0:
            return Bot.roll_dice_from_text(self.kosc_obrazen)
        else:
            return Bot.roll_dice_from_text(obrazenia)
    """
    na razie część amunicji zrobiona (ppanc gotowa, wyborowa gotowa, podźwiękowa gotowa)
    """
    def __dostosuj_specjalna_amunicje(self):
        if self.typ_amunicji == "podstawowa":
            return 0
        elif self.typ_amunicji == "wyborowa":
            self.maks_zasieg_amunicji = 1000
            self.cena = self.cena * 3
        elif self.typ_amunicji == "przeciwpancerna":
            self.cena = self.cena * 3
            self.penetracja = self.penetracja + 1
            if self.charakterystyka_naboju == "pistoletowe":
                self.kosc_obrazen = "d4"
            if self.charakterystyka_naboju == "pośrednie": #w pliku są polskie znaki!!!
                self.kosc_obrazen = "d6"
            if self.charakterystyka_naboju == "rewolwerowe":
                self.kosc_obrazen = "d6"
        elif self.typ_amunicji == "grzybkująca":
            self.cena = self.cena * 3   # done
            self.penetracja = 0
        elif self.typ_amunicji == "wyborowa dalekodystansowa":
            self.cena = self.cena * 3
            self.maks_zasieg_amunicji = 4000
            #mozna przejsc na ciekawsze zasady specjalnej amunicji
        elif self.typ_amunicji == "breneka":
            self.cena = self.cena * 1
        elif self.typ_amunicji == "sportowa":
            self.cena = self.cena * 1
            self.kosc_obrazen = "d" + str(int(self.kosc_obrazen[1]) - 4)
            self.odrzut = int(self.odrzut / 3) * 2
            if self.odrzut % 3 > 0:
                self.odrzut = self.odrzut + 1
        elif self.typ_amunicji == "na strzałki":
            self.cena = self.cena * 5
            self.specjalne.append("wytłumiona")
        elif self.typ_amunicji == "poddźwiękowa":
            self.cena = self.cena * 2
            self.specjalne.append("wytłumiona")
        elif self.typ_amunicji == "gumowe kule":
            self.cena = self.cena * 2   # w tym momencie nie ma możliwości implementacji w tym wydaniu.
            self.specjalne.append("wytłumiona")
        elif self.typ_amunicji == "9mm++":
            self.cena = self.cena * 7.5
            self.odrzut = -4
            self.penetracja = 2


# na razie da się wyłądować amunicje do dowolnej paczki. i dowolną amunicję do dowolnego magazynka.
class Magazynek():
    stan_nabojow: int = 0
    maksymalna_pojemnosc: int = 0
    amunicja = []
    rodzina = ""
    typ_magazynka = ""

    def __init__(self, bron, typ="", naboje_z_paczki_amunicji=""):
        self.maksymalna_pojemnosc = bron.statystyki_podstawowe[9]
        self.__zaladuj_rodzine_i_typ(bron, typ)

    """
    cheks if magazine WHICH YOU BUY is special for purposes of avaibility of feeding another gun
    """
    #TODO NIE MA:typów taśm, podziału na pistoletowe, łudeczek, ani obsługi zintegrowqanych magazynkóW!!!
    def __zaladuj_rodzine_i_typ(self, bron, typ):
        podstawowy_jest_specjalny = False
        for i in bron.zasady_specjalne:
            if i in ("ar", "sr25", "g36", "glock", "g3", "as", "akm", "ak74"):
                self.rodzina = i
            if i in ("powiększone magazynki", "taśma", "taśma i stanagi", "bębnowy magazynek", "łódeczki"):
                self.typ_magazynka = i
                podstawowy_jest_specjalny = True
                if typ == "":
                    typ = i
                if i == "taśma i stanagi":
                    self.typ_magazynka = "taśma"
                    if typ == "":
                        typ = i
        if self.rodzina == "":
            self.rodzina = bron.statystyki_podstawowe[0]
        if typ == "":
            return True
        if typ == "podstawowy":
            if podstawowy_jest_specjalny:
                if self.typ_magazynka in ("powiększone magazynki", "bębnowy magazynek"):
                    self.typ_magazynka = typ
                    self.maksymalna_pojemnosc = 30
                    return True
        if typ == "powiększone magazynki":
            if podstawowy_jest_specjalny:
                if self.typ_magazynka in ("bębnowy magazynek"):
                    self.typ_magazynka = typ
                    self.maksymalna_pojemnosc = 45
                    return True
        else:
            self.typ_magazynka = typ
            self.maksymalna_pojemnosc = int(self.maksymalna_pojemnosc * 1.5)
            return True
        if typ == "bębnowy magazynek":
            for i in bron.zasady_specjalne:
                if i in ("pistolet", "pistolet maszynowy"):
                    self.typ_magazynka = typ
                    self.maksymalna_pojemnosc = 50
                    return True
                if i == "strzelba":
                    self.typ_magazynka = typ
                    self.maksymalna_pojemnosc = 32
                    return True
            self.typ_magazynka = typ
            self.maksymalna_pojemnosc = 100
            return True

    """
    cheks if magazine is special for purposes of avaibility of feeding another gun, to be checked after reload
    """
    def sprawdz_rodzine(self, bron):
        for i in bron.zasady_specjalne:
            if i in ("ar", "sr25", "g36", "glock", "g3", "as", "akm", "ak74"):
                if self.rodzina == i:
                    return True
        if self.rodzina == bron[0]:
            return True
        return False

    """
    it's all about loading magazine with ammo.
    """
    def zaladuj_magazynek(self, paczka_amunicji):
        if self.amunicja == []:
            if paczka_amunicji.ilosc_amunicji > self.maksymalna_pojemnosc:
                paczka_amunicji.ilosc_amunicji = paczka_amunicji.ilosc_amunicji - \
                                                 (self.maksymalna_pojemnosc - self.stan_nabojow)
                self.stan_nabojow = self.maksymalna_pojemnosc
                self.amunicja = paczka_amunicji
                return True
            else:
                self.amunicja = paczka_amunicji
                self.stan_nabojow = paczka_amunicji.ilosc_amunicji
                paczka_amunicji.ilosc_amunicji = 0
                self.amunicja = paczka_amunicji
                return True
        if paczka_amunicji.ilosc_amunicji > (self.maksymalna_pojemnosc - self.stan_nabojow):
            if self.amunicja.nazwa_amunicji == paczka_amunicji.nazwa_amunicji:
                paczka_amunicji.ilosc_amunicji = paczka_amunicji.ilosc_amunicji - (self.maksymalna_pojemnosc - self.stan_nabojow)
                self.stan_nabojow = self.maksymalna_pojemnosc
                return True
            else:
                if self.stan_nabojow == 0:
                    self.amunicja = paczka_amunicji
                    paczka_amunicji.ilosc_amunicji = paczka_amunicji.ilosc_amunicji - (
                                self.maksymalna_pojemnosc - self.stan_nabojow)
                    self.stan_nabojow = self.maksymalna_pojemnosc
                    return True
                else:
                    Bot.output("Proba zaladowania inna amunicja niz dotychczas! \n"
                               " rozladuj magazynek nim zaladujesz nowa amunicja!")
                    return False
        else:
            if self.stan_nabojow != 0:
                if self.amunicja.nazwa_amunicji == paczka_amunicji.nazwa_amunicji:
                    Bot.output("wlasnie skonczyla sie paczka amunicji")
                else:
                    Bot.output("Proba zaladowania inna amunicja niz dotychczas! \n"
                               " rozladuj magazynek nim zaladujesz nowa amunicja!")
                    return False
            self.stan_nabojow = self.stan_nabojow + paczka_amunicji.ilosc_amunicji
            self.amunicja = paczka_amunicji
            paczka_amunicji.ilosc_amunicji = 0

    """
    unloads the ammo to the selected ammunition
    """
    def wyladuj_amunicje(self, paczka_amunicji):
        if self.amunicja.nazwa_amunicji == paczka_amunicji.nazwa_amunicji:
            paczka_amunicji.ilosc_amunicji = paczka_amunicji.ilosc_amunicji + self.stan_nabojow
            self.stan_nabojow = 0
            return True
        return False


class Bron(Przedmiot):
    rodzaj_testu = ""
    kosc_obrazen = ""
    premia = 0
    penetracja = 0
    zasieg_maksymalny = 0
    zasady_specjalne = []

    def __init__(self, rodzaj_testu, kosc_obrazen, premia, penetracja, zasieg_maksymalny, masa=3, cena=0):
        super(Bron, self).__init__(masa, cena)
        self.rodzaj_testu = rodzaj_testu
        self.kosc_obrazen = kosc_obrazen
        self.premia = premia
        self.penetracja = self.penetracja_to_int(penetracja)
        self.zasieg_maksymalny = zasieg_maksymalny

    def rzut_na_obrazenia(self):
        return Bot.roll_dice_from_text(self.kosc_obrazen)

    def test_obrazen_z_egzekucja(self, cel, premia=0):
        cel.rana(self.rzut_na_obrazenia() + premia, self.penetracja)

    def test_trafienia(self, operator, cel, dodatkowe, zasieg=0):
        wynik = operator.rzut_na_umiejetnasc(self.rodzaj_testu) + self.aktualna_premia(operator, zasieg) + dodatkowe - cel.aktualny_unik()
        if wynik >= 0:
            return wynik
        else:
            raise Exception('chybiles!')

    def aktualna_premia(self, operator, zasieg):
        if zasieg <= self.zasieg_maksymalny:
            return 0 #self.premia - zasieg
        raise Exception('cel jest po za zasiegiem.')

    def penetracja_to_int(self, penetracja):
        return constants.penetracja[penetracja]

    def oczysc_zasady_specjalne(self):
        for i in range(0, len(self.zasady_specjalne)):
            self.zasady_specjalne[i] = self.zasady_specjalne[i].strip()


# TODO specjalna amunicja, zasady specjalne broni, możliwość wpływu specjalizacji.
class BronStrzelecka(Bron): #pełne pokrycie

    statystyki_podstawowe: list = []
    statystyki_celownika: list = []
    zasieg_przyrost = 0
    zasieg_minimalny = 0
    aktualny_magazynek = []
    naboj_w_komorze = False
    szybkostrzelnosc = 0
    odrzut_aktualny = 0
    walka_wrecz = []
    porecznosc = 0
    wymienny_magazynek = 0
    rostawiona = False
    kara_za_nierostawienie = 0
    czas_rostawienia = 0
    awaria = False
    zacinka = False
    zlozony_do_strzalu = False
    celownik = []
    szyny_montazowe = []

    #defaultowo ma muszczkę i szczerbinkę.
    def __init__(self, bron, celownik=Celownik(('zwykłe', 0, 25, '', 'w nocy kara -4,', 2, 0, '-')), amunicja=("podstawowa"), magazynek=""):
        super(BronStrzelecka, self).__init__("strzelectwo", bron[5], bron[3], bron[6], bron[1], bron[13], bron[14])
        self.statystyki_podstawowe = bron
        self.__nastaw_celownik(celownik)
        self.amunicja = amunicja
        self.naboj_w_komorze = False
        if magazynek == "":
            self.aktualny_magazynek = Magazynek(self)
            self.wymienny_magazynek = True
        self.zasady_specjalne = bron[7].split(",")
        self.oczysc_zasady_specjalne()
        for i in self.zasady_specjalne:
            if i in ("podwójny magazynek rurowy", "magazynek rurowy", "łódeczki"):
                self.__zamontuj_magazynek_staly()
        self.szybkostrzelnosc = bron[2]
        self.walka_wrecz = BronBiala(['kolba', 0, 0, 0, 0, 'd2', 'x', 'obuchowa', '$0,00'])
        self.__nastaw_kare_za_nierostawienie()
        self.awaria = False
        self.zacinka = False
        self.zlozony_do_strzalu = False
        self.celownik = celownik
        self.szyny_montazowe = [[], [], [], []]
        self.__przygotuj_miejsca_do_zamontowania()

    def __przygotuj_miejsca_do_zamontowania(self):
        dozwolone_dodatki = str(self.statystyki_podstawowe[11])
        if dozwolone_dodatki.startswith('0/'):
            for i in range(0, int(dozwolone_dodatki[2])):
                self.szyny_montazowe[i] = "wykup"
            for i in range(0, len(self.szyny_montazowe)):
                if not self.szyny_montazowe[i]:
                    self.szyny_montazowe[i] = "nie"
        if dozwolone_dodatki == "dolna":
            self.szyny_montazowe = ["nie", "tak", "nie", "nie"]
            return True
        if dozwolone_dodatki in ("nie", "0"):
            self.szyny_montazowe = ["nie", "nie", "nie", "nie"]
        return True

    def dokup_szyny(self, operator):
        if operator.pieniadze < 300:
            Bot.output("Nie masz dość forsy")
            return False
        operator.pieniadze =operator.pieniadze - 300            #zafiksowana cena szyn dodatkowych
        for i in range(0, len(self.szyny_montazowe)):
            if self.szyny_montazowe[i] == "wykup":
                self.szyny_montazowe[i] = "tak"
        return True

    def zamontuj_dodatek(self, dodatek):
        return dodatek.zaloz(self)

    def zdejmij_dodatek(self, nazwa_dodatku):
        for i in range(0,len(self.szyny_montazowe)):
            if self.szyny_montazowe[i].nazwa == nazwa_dodatku:
                self.szyny_montazowe[i].zdejmij(self)


    def __zamontuj_magazynek_staly(self):
        self.wymienny_magazynek = False

    def __nastaw_kare_za_nierostawienie(self):
        self.kara_za_nierostawienie = -1
        if "kobyła" in self.zasady_specjalne:
            self.kara_za_nierostawienie = -10
        if "ciężka" in self.zasady_specjalne:
            self.kara_za_nierostawienie = -4
        if "poręczna" in self.zasady_specjalne:
            self.kara_za_nierostawienie = 0

    def rostaw_bron(self):
        self.rostawiona = True
        return self.czas_rostawienia

    def odrzut(self, opetator):
        redukcja = self.odrzut_aktualny + opetator.mod_sila
        if redukcja < 0:
            return redukcja
        else:
            return 0

    def rzut_na_obrazenia(self):
        return Bot.roll_dice_from_text(self.kosc_obrazen)

    def test_obrazen_z_egzekucja(self, cel, premia, dystans):
        if "potezna" in self.zasady_specjalne:
            premia = premia * 2
        self.aktualny_magazynek.amunicja.zadaj_obrazenia(cel, premia, dystans)

    def test_trafienia(self, operator, cel, tryb, dodatkowe, zasieg):
        #potrzeba dodatkowe odrzuty policzyć
        if tryb in ("samoczynny", "serie"):
            dodatkowe = dodatkowe + self.__dodatkowy_odrzut_ognia_samoczynnego(tryb)
        return super(BronStrzelecka, self).test_trafienia(operator, cel, dodatkowe, zasieg)

    def __dodatkowy_odrzut_ognia_samoczynnego(self, tryb):
        dodatkowa_redukcja = 0
        if "stabilny ostrzał" in self.zasady_specjalne:
            for i in self.zasady_specjalne:
                if "stabilny ostrzał" in i:
                    dodatkowa_redukcja = int(i[-1])
        if tryb == "serie":
            if dodatkowa_redukcja < int(self.odrzut_aktualny/2):
                return 0
            else:
                return int(int(self.odrzut_aktualny)/2 + dodatkowa_redukcja)
        if tryb == "samoczynny":
            if dodatkowa_redukcja < int(self.odrzut_aktualny):
                return 0
            else:
                return int(self.odrzut_aktualny) + dodatkowa_redukcja



    def __interpretuj_zasady_bazujace_na_amunicji(self, zasięg): #nie przetestowana
        premia = 0
        if "snajperka" in self.zasady_specjalne:
            if self.aktualny_magazynek.amunicja.typ_amunicji == "wyborowa":
                premia = premia + 1
            if self.aktualny_magazynek.amunicja.typ_amunicji == "wybitnie wyborowa":
                premia = premia + 1
        if "duzy kaliber" in self.zasady_specjalne:
            if self.aktualny_magazynek.amunicja.typ_amunicji == "wyborowa":
                premia = premia + 1
            if self.aktualny_magazynek.amunicja.typ_amunicji == "wybitnie wyborowa":
                premia = premia + 1
        if "strzelba" in self.zasady_specjalne:
            if self.aktualny_magazynek.amunicja.typ_amunicji == "podstawowa":
                if zasięg <= 15:
                    premia = premia + 3
                if zasięg <= 5:
                    premia = premia + 2
        return premia

    def __specjalne_kary_za_odleglosc(self, operator, odleglosc):
        if self.zlozony_do_strzalu & (self.celownik.zasieg_minimalny < odleglosc):
            kara = odleglosc / self.celownik.przyrost_zasiegu
            kara = kara * 2 - self.celownik.premia
            if "pistolet" in self.zasady_specjalne:
                if self.celownik.typ == "mechaniczne":
                    kara = odleglosc / (self.celownik.przyrost_zasiegu - 5)
                    kara = kara * 4 - self.celownik.premia
                    return kara
                kara = odleglosc / self.celownik.przyrost_zasiegu
                kara = kara * 2 - self.celownik.premia
            return kara
        else:
            kara = odleglosc / operator.zwroc_naturalny_przyrost_zasiegu()
            kara = kara * 5
            return kara

    def aktualna_premia(self, operator, odleglosc):
        if operator.w_ruchu < -1:
            self.zlozony_do_strzalu = False
        super(BronStrzelecka, self).aktualna_premia(operator, odleglosc)
        if odleglosc > self.aktualny_magazynek.amunicja.maks_zasieg_amunicji:
            raise Exception('cel jest po za zasiegiem.')
        kara_za_zasieg = self.__specjalne_kary_za_odleglosc(operator, odleglosc)
        if 1 < self.zasieg_minimalny < 5:
            kara_za_zasieg = kara_za_zasieg * self.zasieg_minimalny
        premia = int(self.premia)
        premia = premia + int(self.odrzut(operator))
        premia = premia - int(kara_za_zasieg)
        premia = premia + self.__interpretuj_zasady_bazujace_na_amunicji(odleglosc)
        if "celna" in self.zasady_specjalne:
            if operator.umiejetnosci[constants.UmiejetnasciDoInt["strzelectwo"]][0] > 2:
                premia = premia + 1
        if "wybitnie celna" in self.zasady_specjalne:
            if operator.umiejetnosci[constants.UmiejetnasciDoInt["strzelectwo"]][0] > 2:
                premia = premia + 1
            if operator.umiejetnosci[constants.UmiejetnasciDoInt["strzelectwo"]][0] > 4:
                premia = premia + 1
        if not self.rostawiona:
            premia = premia + self.kara_za_nierostawienie
        if self.rostawiona:
            if self.kara_za_nierostawienie == 0:
                premia = premia + 1
        return premia

    def zloz_sie_do_strzalu(self):
        self.zlozony_do_strzalu = True

    def zmien_celownik(self, celownik):
        self.__nastaw_celownik(celownik)

    def __nastaw_celownik(self, celownik):
        self.celownik = celownik
        self.zasieg_przyrost = self.celownik.przyrost_zasiegu

    def zmien_magazynek(self, magazynek):
        if not self.wymienny_magazynek:
            if magazynek.typ_magazynka == "łódeczki":
                pustka = self.aktualny_magazynek.maksymalna_pojemnosc - self.aktualny_magazynek.stan_nabojow
                if magazynek.stan_nabojow >= pustka:
                    if self.aktualny_magazynek.stan_nabojow == 0:
                        self.aktualny_magazynek.amunicja = magazynek.amunicja
                        self.kosc_obrazen = magazynek.amunicja.kosc_obrazen
                        self.penetracja = magazynek.amunicja.penetracja
                        self.odrzut_aktualny = magazynek.amunicja.odrzut
                    self.aktualny_magazynek.stan_nabojow = self.aktualny_magazynek.stan_nabojow + pustka
                    magazynek.stan_nabojow = magazynek.stan_nabojow - pustka
                else:
                    self.aktualny_magazynek.stan_nabojow = self.aktualny_magazynek.stan_nabojow + magazynek.stan_nabojow
                    magazynek.stan_nabojow = 0
                return True
            return False
        odloz = self.aktualny_magazynek
        self.aktualny_magazynek = magazynek
        self.kosc_obrazen = magazynek.amunicja.kosc_obrazen
        self.penetracja = magazynek.amunicja.penetracja
        self.odrzut_aktualny = magazynek.amunicja.odrzut
        return odloz

    def zaciagnij_naboj(self):
        try:
            if self.aktualny_magazynek.amunicja.nazwa_naboju == self.statystyki_podstawowe[8]:
                if self.aktualny_magazynek.stan_nabojow > 0:
                    self.aktualny_magazynek.stan_nabojow = self.aktualny_magazynek.stan_nabojow - 1
                    self.naboj_w_komorze = True
                    return True
                else:
                    Bot.output("nie masz dosc nabojow w magazynku!")
                    return False
            else:
                Bot.output("Naboje nie pasuja do broni!")
                return False
        except AttributeError:
            if not self.aktualny_magazynek.amunicja:
                Bot.output("magazynek nie jest zaladowany nabojami!")
                return False
            raise AttributeError

    def rzut_na_awarie(self):
        kosc_rzutu = 10
        if "bezawaryjna" in self.zasady_specjalne:
            kosc_rzutu = 100
        result = Bot.roll_dice(kosc_rzutu)
        if result == 1:
            self.naboj_w_komorze = False
            kosc_rzutu = 10
            if "niezniszczalna" in self.zasady_specjalne:
                kosc_rzutu = 100
            result = Bot.roll_dice(kosc_rzutu)
            if result == 1:
                self.awaria = True

# TODo zasady specjalne broni, możliwość wpływu specjalizacji.
class BronBiala(Bron):

    def __init__(self, bron):
        #(self, rodzaj_testu, kosc_obrazen, premia, penetracja, zasieg_maksymalny):
        super(BronBiala, self).__init__("walka wrecz", bron[5], bron[3], bron[6], bron[1])
        self.statystyki_podstawowe = bron

    def test_trafienia(self, operator, cel, zasieg=0, dodatkowe=0):
        wynik = operator.rzut_na_umiejetnasc(self.rodzaj_testu)
        wynik = wynik + self.premia
        if wynik > cel.rzut_na_umiejetnasc(self.rodzaj_testu):
            if wynik >= cel.bazowy_unik / 2:
                self.test_obrazen_z_egzekucja(cel)
                return True
            else:
                raise Exception('walczysz lepiej od wroga, ale wciąż nie jesteś w stanie go trafić')
        else:
            raise Exception('przeciwnik lepiej walczy')
