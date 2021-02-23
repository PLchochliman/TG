import hero
import items as items
import Bot as Bot


class akcje():
    costam = 0


class WalkaWrecz(akcje):
    def uderz(self, operator, cel, zasieg=0): # TODO bez testow!!!!!
        try:
            wynik = operator.rzut_na_umiejetnasc("walka wrecz")
            if operator.aktywna_bron.zasieg_maksymalny < 2:
                wynik = wynik + operator.aktywna_bron.premia
            odpowiedz = cel.rzut_na_umiejetnasc("walka wrecz")
            if cel.aktywna_bron.zasieg_maksymalny < 2:
                odpowiedz = odpowiedz + cel.aktywna_bron.premia
            if wynik > odpowiedz:
                if wynik >= cel.bazowy_unik / 2:
                    self.test_obrazen_z_egzekucja(cel)
                    return True
                else:
                    raise Exception('walczysz lepiej od wroga, ale wciąż nie jesteś w stanie go trafić')
            else:
                raise Exception('przeciwnik lepiej walczy')
        except Exception as inst:
            powod = inst.args[0]
            Bot.output('Na celu nie zrobilo to zadnego wrazenia bo ' + powod)


class Shooting(akcje):
    @staticmethod
    def strzal(operator, cel, odleglosc):
        return 0

    """
    failuje w momencie kiedy operator nie moze trafic celu.
    """

    def test_trafienia(self, operator, cel, dodatkowe, zasieg):
        return operator.aktywna_bron.test_trafienia(operator, cel, dodatkowe, zasieg)

    def __sprawdzenie_czy_mozna_strzelac(self, operator, tryb):
        if not operator.aktywna_bron.naboj_w_komorze:
            raise Exception("brak naboju w komorze.\nPo nacisnieciu spustu nic sie nie stalo.")
        if tryb in ("samoczynny", "serie"):
            if operator.aktywna_bron.statystyki_podstawowe[2] in ("sa", "ba", "bu"):
                tryb = "pojedynczy"
                Bot.output("Po nacisnieciu spustu, lufę opóścił tylko 1 nabój. "
                           "Następnym razem sprawdź z czego strzelasz")


    def __zadaj_obrazenia(self, cel, bron, premia=0, ilosc_trafien=1):
        for i in range(0, ilosc_trafien):
            bron.test_obrazen_z_egzekucja(cel, int(premia))


# oraz nie daje możliwości do strzelania 2 wrogów naRaz.
# nie sprawdza równierz kar za różne zasięgi.
    def strzelaj(self, operator, cel, zasieg, tryb="pojedynczy"):
        try:
            if tryb not in ("pojedynczy", "pelne skupienie", "samoczynny", "serie"):
                raise Exception("nie ma takiego trybu. Dostępne tryby to: pojedynczy, pelne skupienie, samoczynny, serie")
            self.__sprawdzenie_czy_mozna_strzelac(operator, tryb)
            dodatkowe = 0
            if tryb == "pelne skupienie":
                dodatkowe = Bot.roll_dice_from_text("3d6")
                zasieg = zasieg/2
            wynik = self.test_trafienia(operator, cel, dodatkowe, zasieg) #failuje juz z wyjatku testu trafienia
            if wynik > 0:
                wynik = int(wynik)
                ilosc_trafien = self.__zuzycie(operator.aktywna_bron, tryb, wynik)
                if tryb in ("pojedynczy", "pelne skupienie"):
                    if wynik > 10:
                        cel.rana(11)
                    else:
                        premia = wynik / 3
                        self.__zadaj_obrazenia(cel, operator.aktywna_bron, int(premia))
                        return True
                self.__zadaj_obrazenia(cel, operator.aktywna_bron, 0, ilosc_trafien)
                return wynik
            else:
                operator.aktywna_bron.test_obrazen_z_egzekucja(cel)
                return True
        except Exception as inst:
            powod = inst.args[0]
            Bot.output(cel.imie + " nie oberwal bo " + powod)
            return False

    def __zuzycie(self, bron, tryb, proponowana_libcza_naboi=1):
        realnie_wystrzelone_naboje = 0
        if proponowana_libcza_naboi > bron.szybkostrzelnosc:
            proponowana_libcza_naboi = bron.szybkostrzelnosc
        if tryb == "serie":
            if proponowana_libcza_naboi > 3:
               proponowana_libcza_naboi = 3
        if tryb in ("pelne skupienie", "pojedynczy"):
            proponowana_libcza_naboi = 1
            if bron.statystyki_podstawowe[2] in ("ba", "bu"):
                bron.naboj_w_komorze = False
                return 1
        if bron.aktualny_magazynek.stan_nabojow >= proponowana_libcza_naboi:
            bron.aktualny_magazynek.stan_nabojow = bron.aktualny_magazynek.stan_nabojow - proponowana_libcza_naboi
            realnie_wystrzelone_naboje = proponowana_libcza_naboi
        else:
            realnie_wystrzelone_naboje = bron.aktualny_magazynek.stan_nabojow + 1
            bron.aktualny_magazynek.stan_nabojow = 0
            bron.naboj_w_komorze = 0
            if tryb in ("samoczynny", "serie"):
                Bot.output("podczas prowadzenia ognia, karabin przestał strzelać")
        return realnie_wystrzelone_naboje




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