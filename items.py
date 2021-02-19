import excelDigger as Excel
import Bot as Bot
import constans as constants
import hero as hero
#kurwa mamy to


class Przedmioty(): #pełne pokrycie
    dane = []

    def __init__(self, CoDoQRWY):
        self.przetwornik = Excel.Loader('TabelaBroni.xlsx', ['bron', 'bronbiala', 'granaty', 'celowniki'],
                                        ['O300', 'I19', 'I10', 'G28'])
        self.dane = self.przetwornik.zwroc()

    def luskacz_broni(self, nazwaBroni):
        for i in self.dane[2]:
            if i[0] == nazwaBroni:
                return i
        return False

    def luskacz_broni_bialej(self, nazwaBroni):
        for i in self.dane[3]:
            if i[0] == nazwaBroni:
                return i
        return False

    def luskacz_granatow(self, nazwaBroni):
        for i in self.dane[4]:
            if i[0] == nazwaBroni:
                return i
        return False

    def luskacz_celownikow(self, nazwaBroni):
        for i in self.dane[5]:
            if i[0] == nazwaBroni:
                return i
        return False



class Bron: #pełne pokrycie
    rodzaj_testu = ""
    kosc_obrazen = ""
    premia = 0
    penetracja = 0
    zasieg_maksymalny = 0

    def __init__(self, rodzaj_testu, kosc_obrazen, premia, penetracja, zasieg_maksymalny):
        self.rodzaj_testu = rodzaj_testu
        self.kosc_obrazen = kosc_obrazen
        self.premia = premia
        self.penetracja = self.penetracja_to_int(penetracja)
        self.zasieg_maksymalny = zasieg_maksymalny

    def rzut_na_obrazenia(self):
        return Bot.roll_dice_from_text(self.kosc_obrazen)

    def zadaj_obrazenia(self, cel):
        cel.rana(self.rzut_na_obrazenia(), self.penetracja)

    def test_trafenia(self, operator, cel, zasieg=0):
        if (operator.rzut_na_umiejetnasc(self.rodzaj_testu) + self.aktualna_premia(operator, zasieg)) >= cel.unik:
            self.zadaj_obrazenia(cel)
            return True
        else:
            raise Exception('chybiles!')

    def aktualna_premia(self, operator, zasieg):
        if zasieg <= self.zasieg_maksymalny:
            return self.premia - zasieg
        raise Exception('cel jest po za zasiegiem.')

    def atakuj(self, operator, cel, zasieg):
        try:
            return self.test_trafenia(operator, cel, zasieg)
        except Exception as inst:
            powod = inst.args[0]
            Bot.output('Na celu nie zrobilo to zadnego wrazenia bo ' + powod)

    def penetracja_to_int(self, penetracja):
        return constants.penetracja[penetracja]


class BronStrzelecka(Bron): #pełne pokrycie

    statystyki_podstawowe: list = []
    statystyki_celownika: list = []
    zasieg_przyrost = 0
    zasieg_minimalny = 0

# if is smaller than 5 then it makes work for increased penalty for range, because of shit instead of sights

    def __init__(self, bron, celownik=['zwykłe', 0, 25, '', 'w nocy kara -4,', 0, '-']):
        super(BronStrzelecka, self).__init__("strzelectwo", bron[5], bron[3], bron[6], bron[1])
        self.statystyki_podstawowe = bron
        self.nastaw_celownik(celownik)

    def odrzut(self, opetator):
        redukcja = self.statystyki_podstawowe[4] + opetator.mod_sila
        if redukcja < 0:
            return redukcja
        else:
            return 0

    def test_trafenia(self, operator, cel, zasieg):
        super(BronStrzelecka, self).test_trafenia(operator, cel, zasieg)

    def aktualna_premia(self, operator, odległosc):
        kara_za_zasieg = odległosc / self.zasieg_przyrost
        if 1 < self.zasieg_minimalny < 5:
            kara_za_zasieg = kara_za_zasieg * self.zasieg_minimalny
        premia = self.premia + self.odrzut(operator) - int(kara_za_zasieg)
        return premia

    def zmien_celownik(self, celownik):
        self.premia = self.premia - self.statystyki_celownika[1]
        self.statystyki_celownika = celownik
        self.premia = self.premia + self.statystyki_celownika[1]
        self.zasieg_przyrost = self.statystyki_celownika[2]

    def nastaw_celownik(self, celownik):
        self.statystyki_celownika = celownik
        self.zasieg_przyrost = self.statystyki_celownika[2]
        self.premia = self.premia + self.statystyki_celownika[1]


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

    def test_trafenia(self, operator, cel, zasieg=0):
        wynik = operator.rzut_na_umiejetnasc(self.rodzaj_testu)
        wynik = wynik + self.premia
        if wynik > cel.rzut_na_umiejetnasc(self.rodzaj_testu):
            if wynik >= cel.bazowy_unik /2:
                self.zadaj_obrazenia(cel)
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