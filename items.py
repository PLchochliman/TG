import excelDigger as Excel
import Bot as Bot
import constans as constants
import hero as hero
#kurwa mamy to


class Przedmioty():
    dane = []

    def __init__(self, CoDoQRWY):
        self.przetwornik = Excel.loader('TabelaBroni.xlsx', ['bron', 'bronbiala', 'granaty', 'lunety', 'celowniki'],
                                        ['O300', 'I19', 'I10', 'F13', 'G14'])
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

    def luskacz_lunet(self, nazwaBroni):
        for i in self.dane[5]:
            if i[0] == nazwaBroni:
                return i
        return False

    def luskacz_celownikow(self, nazwaBroni):
        for i in self.dane[6]:
            if i[0] == nazwaBroni:
                return i
        return False


class Bron():
    rodzaj_testu = ""
    kosc_obrazen = ""
    premia = 0
    penetracja = 0

    def __init__(self, rodzaj_testu, kosc_obrazen, premia, penetracja):
        self.rodzaj_testu = rodzaj_testu
        self.kosc_obrazen = kosc_obrazen
        self.premia = premia
        self.penetracja = self.penetracja_to_int(penetracja)

    def rzut_na_obrazenia(self):
        return Bot.roll_dice_from_text(self.kosc_obrazen)

    def zadaj_obrazenia(self, cel):
        cel.rana(self.rzut_na_obrazenia(), self.penetracja)

    def test_trafenia(self, operator, cel):
        if (operator.rzut_na_umiejetnasc(self.rodzaj_testu) + self.aktualna_premia(operator)) >= cel.unik:
            self.zadaj_obrazenia(cel)
            return True
        else:
            return False

    def aktualna_premia(self, operator):
        return self.premia

    def atakuj(self, operator, cel):
        return self.test_trafenia(operator, cel)

    def penetracja_to_int(self, penetracja):
        return constants.penetracja[penetracja]



class BronStrzelecka(Bron):

    statystyki_podstawowe:list = []

    def __init__(self, bron):
        super(BronStrzelecka, self).__init__("strzelectwo", bron[5], bron[3], bron[6])
        self.statystyki_podstawowe = bron


    def odrzut(self, opetator):
        redukcja = self.statystyki_podstawowe[4] + opetator.modSila
        if redukcja < 0:
            return redukcja
        else:
            return 0

    def test_trafenia(self, operator, cel):
        super(BronStrzelecka, self).test_trafenia(operator, cel)

    def aktualna_premia(self, operator):
        premia = self.premia + self.odrzut(operator)
        return premia

"""
itemki = Przedmioty("")
m4ka = itemki.luskaczBroni("m4a1")
M4KA = BronStrzelecka(m4ka)
wojtek = hero.Postac(8, 8, 8, ["bron boczna", "karabiny", "bron krotka"])
beben = hero.Postac(8, 8, 8, ["bron boczna", "karabiny", "bron krotka"])
M4KA.atakuj(wojtek, beben)
"""