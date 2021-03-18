import hero
import items as items
import Bot as Bot


class Akcje():
    # teoretyczniue to w tym się wszystko będzie rozgrywać....
    tura = 0
    faza = 0
    walka_wrecz = []
    strzelanie = []

    def __init__(self, tura=0, faza=0):
        self.tura = tura
        self.faza = faza
        self.walka_wrecz = WalkaWrecz()
        self.strzelanie = Strzelanie()

    def kolejna_faza(self, faza=1):
        if faza > 5:
            self.tura = self.tura + int(faza / 6)
            self.kolejna_faza((faza % 6))
            return True
        self.faza = self.faza + faza
        if self.faza > 5:
            self.tura = self.tura + 1
            self.faza = self.faza - 6
        return True


class WalkaWrecz():
    """
    did without tests, and execution is not ready.
    """
    def uderz(self, operator, cel, zasieg=0):
        try:
            bron = []
            if operator.aktywna_bron == []:
                bron = operator.aktywna_bron =\
                    items.BronBiala(['pięść', 0, 0, 0, 0, 'd2', 'x', 'obuchowa', '$0,00'])
            elif type(operator.aktywna_bron) is not items.BronBiala:
                print("gunwo")
                bron = operator.aktywna_bron.walka_wrecz
                print("gunwo")
            else:
                bron = operator.aktywna_bron
            wynik = operator.rzut_na_umiejetnasc("walka wrecz")
            odpowiedz = cel.rzut_na_umiejetnasc("walka wrecz")
            if bron.zasieg_maksymalny < zasieg:
                raise Exception("nie dosięgnąłeś bronią wroga")
            if bron.zasieg_maksymalny < 2:
                print(operator.aktywna_bron.premia)
                wynik = wynik + int(operator.aktywna_bron.premia) #TODO KURWA!!!
            if cel.aktywna_bron == []:
                odpowiedz = odpowiedz
            elif cel.bron.zasieg_maksymalny < 2:
                odpowiedz = odpowiedz + cel.aktywna_bron.premia
            if wynik > odpowiedz:
                if wynik >= cel.bazowy_unik / 2:
                    bron.test_obrazen_z_egzekucja(cel)
                    return True
                else:
                    raise Exception('walczysz lepiej od wroga, ale wciąż nie jesteś w stanie go trafić')
            else:
                raise Exception('przeciwnik lepiej walczy')
        except Exception as inst:
            powod = inst.args[0]
            Bot.output('Na celu nie zrobilo to zadnego wrazenia bo ' + powod)
           # raise inst
            return False


class Strzelanie():
    """
    failuje w momencie kiedy operator nie moze trafic celu. Przekierowuje wszystko do broni na ten moment.
    """

    def __test_trafienia(self, operator, cel, dodatkowe, zasieg):
        return int(operator.aktywna_bron.test_trafienia(operator, cel, dodatkowe, zasieg))

    """
    do check procedure, if you are able to shoot.
    """
    def __sprawdzenie_czy_mozna_strzelac(self, operator, tryb):
        if not operator.aktywna_bron.naboj_w_komorze:
            raise Exception("brak naboju w komorze.\nPo nacisnieciu spustu nic sie nie stalo.")
        if tryb in ("samoczynny", "serie"):
            if operator.aktywna_bron.statystyki_podstawowe[2] in ("sa", "ba", "bu"):
                tryb = "pojedynczy"
                Bot.output("Po nacisnieciu spustu, lufę opóścił tylko 1 nabój. "
                           "Następnym razem sprawdź z czego strzelasz")
        return tryb

    """
    deals damage to "cel", by gun, and additional modifier (if apply), and many times if nessesary.
    """
    def __zadaj_obrazenia(self, cel, bron, dystans, premia=0, ilosc_trafien=1):
        for i in range(0, ilosc_trafien):
            bron.test_obrazen_z_egzekucja(cel, int(premia), dystans)

        """
        implements shooting procedure from TG.
        """
# oraz nie daje możliwości do strzelania 2 wrogów naRaz.
# nie sprawdza równierz kar za różne zasięgi.
    def strzal(self, operator, cel, zasieg, tryb="pojedynczy"):
        try:
            if tryb not in ("pojedynczy", "pelne skupienie", "samoczynny", "serie"):
                raise Exception("nie ma takiego trybu. Dostępne tryby to: pojedynczy, pelne skupienie, samoczynny, serie")
            tryb = self.__sprawdzenie_czy_mozna_strzelac(operator, tryb)
            dodatkowe = 0
            if tryb == "pelne skupienie":
                dodatkowe = Bot.roll_dice_from_text("3d6")
                zasieg = zasieg/2
            wynik = self.__test_trafienia(operator, cel, dodatkowe, zasieg) #failuje juz z wyjatku testu trafienia
            ilosc_trafien = self.__zuzycie(operator.aktywna_bron, tryb)
            if wynik > 0:
                if tryb in ("pojedynczy", "pelne skupienie"):
                    if wynik > 10:
                        cel.rana(11)
                    else:
                        premia = wynik / 3
                        self.__zadaj_obrazenia(cel, operator.aktywna_bron,  zasieg, int(premia))
                        return True
                if wynik > ilosc_trafien:
                    wynik = ilosc_trafien
                self.__zadaj_obrazenia(cel, operator.aktywna_bron, zasieg, 0, wynik)    # dodać tutaj zasięg
                return True
            else:
                operator.aktywna_bron.test_obrazen_z_egzekucja(cel)
                return True
        except Exception as inst:
            powod = inst.args[0]
            Bot.output(cel.imie + " nie oberwal bo " + powod)
            return False

    """
    liczy zuzycie naboi i od razu aplikuje
    """
    def __zuzycie(self, bron, tryb):
        wystrzelone_naboje = 0
        if tryb == "samoczynny":
            self.__zuzyj_naboje(bron, bron.szybkostrzelnosc)
        if tryb == "serie":
            self.__zuzyj_naboje(bron, 3)
        if tryb in ("pelne skupienie", "pojedynczy"):
            wystrzelone_naboje = 1
            if bron.szybkostrzelnosc in ("ba", "bu"):
                bron.naboj_w_komorze = False
                return 1
            self.__zuzyj_naboje(bron, 1)
        return wystrzelone_naboje

    def __zuzyj_naboje(self, bron, maksymalne):
        if maksymalne > bron.aktualny_magazynek.stan_nabojow:
            maksymalne = bron.aktualny_magazynek.stan_nabojow + 1
            bron.aktualny_magazynek.stan_nabojow = 0
            bron.naboj_w_komorze = False
        else:
            bron.aktualny_magazynek.stan_nabojow = bron.aktualny_magazynek.stan_nabojow - maksymalne
        return maksymalne

"""
dzialajacy blok samoczynnech i serii
                if tryb == "samoczynny":
                    if wynik > operator.aktywna_bron.statystyki_podstawowe[2]:
                        wynik = operator.aktywna_bron.statystyki_podstawowe[2]
                    if wynik > operator.aktywna_bron.aktualny_magazynek.stan_nabojow:
                        wynik = operator.aktywna_bron.aktualny_magazynek.stan_nabojow + 1
                        operator.aktywna_bron.aktualny_magazynek.stan_nabojow = 0
                        operator.aktywna_bron.naboj_w_komorze = False
                    else:
                        operator.aktywna_bron.aktualny_magazynek.stan_nabojow = operator.aktywna_bron.aktualny_magazynek.stan_nabojow - wynik
                    self.__zadaj_obrazenia(cel, operator.aktywna_bron, 0, wynik)
                if tryb == 'serie':
                    if wynik > 3:
                        wynik = 3
                    if wynik > operator.aktywna_bron.aktualny_magazynek.stan_nabojow:
                        wynik = int(operator.aktywna_bron.aktualny_magazynek.stan_nabojow) + 1
                        operator.aktywna_bron.aktualny_magazynek.stan_nabojow = 0
                        operator.aktywna_bron.naboj_w_komorze = False
                    else:
                        operator.aktywna_bron.aktualny_magazynek.stan_nabojow =\
                            int(operator.aktywna_bron.aktualny_magazynek.stan_nabojow) - wynik
                    self.__zadaj_obrazenia(cel, operator.aktywna_bron, 0, wynik)
"""

"""
itemki = items_old.Przedmioty('')
m4ka = itemki.luskacz_broni("m4a1")
M4KA = items_old.BronStrzelecka(m4ka)
wojtek = hero.Postac(8, 8, 8, ["bron boczna", "karabiny", "bron krotka"])
"""