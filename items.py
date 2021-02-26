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
                                        ['O300', 'I19', 'I10', 'G28', 'H40'])
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
    precyzyjna_dla:str = ""

    def __init__(self, amunicja, ilosc_paczek=1, typ_amunicji="podstawowa"):
        self.odrzut = amunicja[4]
        self.nazwa_naboju = amunicja[0]
        self.kosc_obrazen = amunicja[5]
        self.penetracja = amunicja[6]
        self.typ_amunicji = typ_amunicji
        self.nazwa_amunicji = self.nazwa_naboju + " " + self.typ_amunicji
        self.ilosc_amunicji = ilosc_paczek * amunicja[2]
        self.ilosc_paczek = ilosc_paczek



# na razie da się wyłądować amunicje do dowolnej paczki. i dowolną amunicję do dowolnego magazynka.
class Magazynek():
    stan_nabojow: int = 0
    maksymalna_pojemnosc: int = 0
    amunicja = []
    rodzina = ""

    def __init__(self, bron, typ="podstawowy", naboje_z_paczki_amunicji=""):
        self.maksymalna_pojemnosc = bron.statystyki_podstawowe[9]
        self.__zaladuj_rodzine(bron)

    """
    cheks if magazine WHICH YOU BUY is special for purposes of avaibility of feeding another gun
    """
    def __zaladuj_rodzine(self, bron):
        for i in bron.zasady_specjalne:
            if i in ("ar", "sr25", "g36", "glock", "g3", "as", "akm", "ak74"):
                self.rodzina = i
        if self.rodzina == "":
            self.rodzina = bron.statystyki_podstawowe[0]

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
            self.zasady_specjalne[i] = self.zasady_specjalne[i].strip




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

# if is smaller than 5 then it makes work for increased penalty for range, because of shit instead of sights
    # TODO do przeróbki
    def __init__(self, bron, celownik=muszka_i_szczerbinka, amunicja=("podstawowa"), magazynek=""):
        super(BronStrzelecka, self).__init__("strzelectwo", bron[5], bron[3], bron[6], bron[1])
        self.statystyki_podstawowe = bron
        self.__nastaw_celownik(celownik)
        self.amunicja = amunicja
        if magazynek == "":
            self.aktualny_magazynek = Magazynek(self)
        self.zasady_specjalne = bron[7].split(",")
        self.oczysc_zasady_specjalne()
        self.szybkostrzelnosc = bron[2]

    def odrzut(self, opetator):
        redukcja = self.odrzut_aktualny + opetator.mod_sila
        if redukcja < 0:
            return redukcja
        else:
            return 0

    def test_trafienia(self, operator, cel, dodatkowe, zasieg):
        return super(BronStrzelecka, self).test_trafienia(operator, cel, dodatkowe, zasieg)

    def aktualna_premia(self, operator, odległosc):
        super(BronStrzelecka, self).aktualna_premia(operator, odległosc)
        kara_za_zasieg = odległosc / self.zasieg_przyrost
        if 1 < self.zasieg_minimalny < 5:
            kara_za_zasieg = kara_za_zasieg * self.zasieg_minimalny
        premia = int(self.premia)
        premia = premia + int(self.odrzut(operator))
        premia = premia - int(kara_za_zasieg)
        return premia

    def zmien_celownik(self, celownik):
        self.premia = self.premia - self.statystyki_celownika[1]
        self.__nastaw_celownik(celownik)

    def __nastaw_celownik(self, celownik):
        self.statystyki_celownika = celownik
        self.zasieg_przyrost = self.statystyki_celownika[2]
        self.premia = self.premia + self.statystyki_celownika[1]

    def zmien_magazynek(self, magazynek):
        odloz = self.aktualny_magazynek
        self.aktualny_magazynek = magazynek
        self.kosc_obrazen = magazynek.amunicja.kosc_obrazen
        self.penetracja = self.penetracja_to_int(magazynek.amunicja.penetracja)
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
            if self.aktualny_magazynek.amunicja == []:
                Bot.output("magazynek nie jest zaladowany nabojami!")
                return False
            raise AttributeError

# TODo zasady specjalne broni, możliwość wpływu specjalizacji.
class BronBiala(Bron):

    def __init__(self, bron):
        #(self, rodzaj_testu, kosc_obrazen, premia, penetracja, zasieg_maksymalny):
        super(BronBiala, self).__init__("walka wrecz", bron[5], bron[3], bron[6], bron[1])
        self.statystyki_podstawowe = bron

    def atakuj(self, operator, cel, zasieg):
        try:
            return self.test_trafenia(operator, cel, zasieg)
        except Exception as inst:
            powod = inst.args[0]
            Bot.output('Na celu nie zrobilo to zadnego wrazenia bo ' + powod)
            return False

    def test_trafienia(self, operator, cel, zasieg=0):
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