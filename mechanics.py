import mortal_hero
import przedmioty_bron as items
import Bot as Bot
import exceptions as exceptions


class Akcje():
    # teoretyczniue to w tym się wszystko będzie rozgrywać....
    tura = 0
    faza = 0
    walka_wrecz = []
    strzelanie = []
    postacie = []

    def __init__(self, postacie=[], tura=0, faza=0):
        self.tura = tura
        self.faza = faza
        self.walka_wrecz = WalkaWrecz()
        self.strzelanie = Strzelanie()
        self.postacie = postacie

    def kolejna_faza(self):
        for postac in self.postacie:
            co_robi = self.__egzekucja_czynnosci(postac, postac.akcja())
            Bot.output(postac.imie + " wykonał " + co_robi)
        self.przesun_faze()

    def __egzekucja_czynnosci(self, postac, czynnosc):
        czynnosci = czynnosc.split()
        if "strzelanie" in czynnosci:
            self.__strzelanie(postac, czynnosci[1])
        return czynnosc


    def __strzelanie(self, postac, wrog="brak"):
        try:
            if wrog == "brak":
                return False
            return self.strzelanie.strzal(postac, self.__rozpoznaj_cel(wrog), self.__zasieg())
        except exceptions.Pudlo:
            Bot.output("nie ma takiego celu!!! GMie popraw. wpisz brak, jeśli sytuacja się zmieniła i nie"
                       " chcesz oddawać tego strzału")
            wrog = Bot.gm_input_for_bot()
            self.__strzelanie(postac, wrog)

    def __zasieg(self):
        return 0

    def __rozpoznaj_cel(self, imie):
        for postac in self.postacie:
            if postac.imie == imie:
                return postac
        raise exceptions.Pudlo("nie ma takiego celu")

    def przesun_faze(self, faza=1):
        if faza > 5:
            self.tura = self.tura + int(faza / 6)
            self.przesun_faze((faza % 6))
            return True
        self.faza = self.faza + faza
        if self.faza > 5:
            self.tura = self.tura + 1
            self.faza = self.faza - 6
        return True

    def ktora_faza(self):
        return [self.tura, self.faza]




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
                raise exceptions.Pudlo("nie dosięgnąłeś bronią wroga")
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
                    raise exceptions.Pudlo('walczysz lepiej od wroga, ale wciąż nie jesteś w stanie go trafić')
            else:
                raise exceptions.Pudlo('przeciwnik lepiej walczy')
        except exceptions.Pudlo as inst:
            powod = inst.args[0]
            Bot.output('Na celu nie zrobilo to zadnego wrazenia bo ' + powod)
           # raise inst
            return False


class Strzelanie():
    """
    failuje w momencie kiedy operator nie moze trafic celu. Przekierowuje wszystko do broni na ten moment.
    """

    def __test_trafienia(self, operator, cel, tryb, dodatkowe, zasieg):
        return int(operator.aktywna_bron.test_trafienia(operator, cel, tryb, dodatkowe, zasieg))

    """
    do check procedure, if you are able to shoot.
    """
    def __sprawdzenie_czy_mozna_strzelac(self, operator, tryb):
        if not operator.aktywna_bron.naboj_w_komorze:
            raise exceptions.NieWystrzelono("brak naboju w komorze.\nPo nacisnieciu spustu nic sie nie stalo.")
        if tryb in ("samoczynny", "serie"):
            if operator.aktywna_bron.szybkostrzelnosc in ("sa", "ba", "bu"):
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
#  kary za zasieg sa juz w broni
    def strzal(self, operator, cel, zasieg, tryb="pojedynczy"):
        try:
            if operator.aktywna_bron.awaria:
                raise exceptions.NieWystrzelono("BRON MA AWARIE")
            if tryb not in ("pojedynczy", "pelne skupienie", "samoczynny", "serie"):
                raise exceptions.NieWystrzelono("nie ma takiego trybu. Dostępne tryby to: "
                                                "pojedynczy, pelne skupienie, samoczynny, serie")
            tryb = self.__sprawdzenie_czy_mozna_strzelac(operator, tryb)
            ilosc_trafien = self.__zuzycie(operator.aktywna_bron, tryb)
            dodatkowe = operator.handling_specialisations_before_hit()
            if tryb == "pelne skupienie":
                dodatkowe = Bot.roll_dice_from_text("3d6")
                zasieg = zasieg/2
            wynik = self.__test_trafienia(operator, cel, tryb, dodatkowe, zasieg)
            # failuje juz z wyjatku testu trafienia
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
                self.__zadaj_obrazenia(cel, operator.aktywna_bron, zasieg, 0, wynik)
                return True
            else:
                self.__zadaj_obrazenia(cel, operator.aktywna_bron, zasieg, 0, wynik)
                return True
        except exceptions.Pudlo as inst:
            powod = inst.args[0]
            Bot.output(cel.imie + " nie oberwal bo " + powod)
            return False
        except exceptions.NieWystrzelono as inst:
            powod = inst.args[0]
            Bot.output(cel.imie + " nie wystrzelil bo " + powod)
            return False
    """
    liczy zuzycie naboi i od razu aplikuje
    """
    def __zuzycie(self, bron, tryb):
        if not bron.naboj_w_komorze:
            raise exceptions.NieWystrzelono("NIE MA NABOJU W KOMORZE")
        wystrzelone_naboje = 0
        if tryb in "samoczynny":
            wystrzelone_naboje = self.__zuzyj_naboje(bron, int(bron.szybkostrzelnosc))
        if tryb in "serie":
            wystrzelone_naboje = self.__zuzyj_naboje(bron, 3)
        if tryb in ("pojedynczy", "pelne skupienie"):
            wystrzelone_naboje = 1
            if bron.szybkostrzelnosc in ("ba", "bu",):
                bron.naboj_w_komorze = False
                return 1
            self.__zuzyj_naboje(bron, 1)
        return wystrzelone_naboje

    @staticmethod
    def __zuzyj_naboje(bron, maksymalne):
        if maksymalne > bron.aktualny_magazynek.stan_nabojow:
            maksymalne = bron.aktualny_magazynek.stan_nabojow + 1
            bron.aktualny_magazynek.stan_nabojow = 0
            bron.naboj_w_komorze = False
        else:
            bron.aktualny_magazynek.stan_nabojow = bron.aktualny_magazynek.stan_nabojow - maksymalne
        return maksymalne
