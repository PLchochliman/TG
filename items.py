import excelDigger as Excel
import Bot as Bot
import constans as constants
import hero as hero

#kurwa bieda, może i lepiej bybyło przedmioty zadeklarować wcześniej ale robiłem to na prosto.
muszka_i_szczerbinka = ('zwykłe', 0, 25, '', 'w nocy kara -4,', 0, '-')

class Przedmioty(): #pełne pokrycie
    dane = []

    """
    loads the guns, and accesories to TG from file
    """

    def __init__(self, CoDoQRWY):
        self.przetwornik = Excel.Loader('TabelaBroni.xlsx', ['bron', 'bronbiala', 'granaty', 'celowniki', 'amunicja'],
                                        ['O300', 'I19', 'I10', 'G28', 'I40'])
        self.dane = self.przetwornik.zwroc()
        self.przetwornik.wyczysc()

    """
    Enable to select single gun
    """

    def luskacz_broni(self, nazwaBroni):
        for i in self.dane[0]:
            if i[0] == nazwaBroni:
                return i
        return False

    """
    enable to select single melee weapon
    """

    def luskacz_broni_bialej(self, nazwaBroni):
        for i in self.dane[1]:
            if i[0] == nazwaBroni:
                return i
        return False

    """
    enable to select single granade
    """

    def luskacz_granatow(self, nazwaBroni):
        for i in self.dane[2]:
            if i[0] == nazwaBroni:
                return i
        return False

    """
    enables to select single scope
    """

    def luskacz_celownikow(self, nazwaBroni):
        for i in self.dane[3]:
            if i[0] == nazwaBroni:
                return i
        return False

    """
    enable to select ammunition
    """

    def luskacz_amunicji(self, nazwa_amunicji):
        for i in self.dane[4]:
            if i[0] == nazwa_amunicji:
                return i
        return False

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
        self.__dostosuj_specjalna_amunicje()

    """
    na razie sama cena
    """
    def __dostosuj_specjalna_amunicje(self):
        if self.typ_amunicji == "podstawowa":
            return 0
        elif self.typ_amunicji == "wyborowa":
            self.maks_zasieg_amunicji = 1000
            self.cena = self.cena * 3
        elif self.typ_amunicji == "przeciwpancerna":
            self.cena = self.cena * 3
        elif self.typ_amunicji == "grzybkująca":
            self.cena = self.cena * 3
        elif self.typ_amunicji == "wyborowa dalekodystansowa":
            self.cena = self.cena * 3
            self.maks_zasieg_amunicji = 3500
            #mozna przejsc na ciekawsze zasady specjalnej amunicji
        elif self.typ_amunicji == "breneka":
            self.cena = self.cena * 1
        elif self.typ_amunicji == "sportowa":
            self.cena = self.cena * 1
        elif self.typ_amunicji == "na strzałki":
            self.cena = self.cena * 5
        elif self.typ_amunicji == "poddźwiękowa":
            self.cena = self.cena * 2
        elif self.typ_amunicji == "gumowe kule":
            self.cena = self.cena * 2
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
            #srobic dla strzelby i pmów!!!
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

class Bron: #pełne pokrycie
    rodzaj_testu = ""
    kosc_obrazen = ""
    premia = 0
    penetracja = 0
    zasieg_maksymalny = 0
    zasady_specjalne = []


    def __init__(self, rodzaj_testu, kosc_obrazen, premia, penetracja, zasieg_maksymalny):
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
        wynik = operator.rzut_na_umiejetnasc(self.rodzaj_testu) + self.aktualna_premia(operator, zasieg) + dodatkowe - cel.unik
        if wynik >= 0:
            return wynik
        else:
            raise Exception('chybiles!')

    def aktualna_premia(self, operator, zasieg):
        if zasieg <= self.zasieg_maksymalny:
            return self.premia - zasieg
        raise Exception('cel jest po za zasiegiem.')

    def penetracja_to_int(self, penetracja):
        return constants.penetracja[penetracja]

    def oczysc_zasady_specjalne(self):
        for i in range(0, len(self.zasady_specjalne)):
            self.zasady_specjalne[i] = self.zasady_specjalne[i].strip()


# TODO specjalna amunicja, zasady specjalne broni, możliwość wpływu specjalizacji. PISTOLETY PMY I INNE takie
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
    # Strzelba, snajperka Pośrednia,

# if is smaller than 5 then it makes work for increased penalty for range, because of shit instead of sights

    def __init__(self, bron, celownik=muszka_i_szczerbinka, amunicja=("podstawowa"), magazynek=""):
        super(BronStrzelecka, self).__init__("strzelectwo", bron[5], bron[3], bron[6], bron[1])
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

    def test_trafienia(self, operator, cel, dodatkowe, zasieg):
        return super(BronStrzelecka, self).test_trafienia(operator, cel, dodatkowe, zasieg)

    def __interpretuj_zasady_bazujace_na_amunicji(self, zasięg): #nie przetestowana
        premia = 0
        if "snajperka" in self.zasady_specjalne:
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

    def __specjalne_kary_za_odleglosc(self, odleglosc):
        kara = odleglosc / self.zasieg_przyrost
        for i in self.zasady_specjalne:
            if i == "pistolet":
                kara = kara * 3
            if i == "pistolet maszynowy":
                kara = kara * 2
        return kara

    def aktualna_premia(self, operator, odległosc):
        super(BronStrzelecka, self).aktualna_premia(operator, odległosc)
        if odległosc > self.aktualny_magazynek.amunicja.maks_zasieg_amunicji:
            raise Exception('cel jest po za zasiegiem.')
        kara_za_zasieg = self.__specjalne_kary_za_odleglosc(odległosc)
        if 1 < self.zasieg_minimalny < 5:
            kara_za_zasieg = kara_za_zasieg * self.zasieg_minimalny
        premia = int(self.premia)
        premia = premia + int(self.odrzut(operator))
        premia = premia - int(kara_za_zasieg)
        premia = premia + self.__interpretuj_zasady_bazujace_na_amunicji(odległosc)
        if not self.rostawiona:
            premia = premia + self.kara_za_nierostawienie
        if self.rostawiona:
            if self.kara_za_nierostawienie == 0:
                premia = premia + 1
        return premia

    def zmien_celownik(self, celownik):
        self.premia = self.premia - self.statystyki_celownika[1]
        self.__nastaw_celownik(celownik)

    def __nastaw_celownik(self, celownik):
        self.statystyki_celownika = celownik
        self.zasieg_przyrost = self.statystyki_celownika[2]
        self.premia = self.premia + self.statystyki_celownika[1]

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


# TODo zasady specjalne broni, możliwość wpływu specjalizacji.
class BronBiala(Bron):

    def __init__(self, bron):
        #(self, rodzaj_testu, kosc_obrazen, premia, penetracja, zasieg_maksymalny):
        super(BronBiala, self).__init__("walka wrecz", bron[5], bron[3], bron[6], bron[1])
        self.statystyki_podstawowe = bron

    """
    def atakuj(self, operator, cel, zasieg):
        try:
            return self.test_trafenia(operator, cel, zasieg)
        except Exception as inst:
            powod = inst.args[0]
            Bot.output('Na celu nie zrobilo to zadnego wrazenia bo ' + powod)
            return False
    """
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

"""
itemki = Przedmioty("")
m4ka = itemki.luskaczBroni("m4a1")
M4KA = BronStrzelecka(m4ka)
wojtek = hero.Postac(8, 8, 8, ["bron boczna", "karabiny", "bron krotka"])
cel = hero.Postac(8, 8, 8, ["bron boczna", "karabiny", "bron krotka"])
M4KA.atakuj(wojtek, cel) ec
"""