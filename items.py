import excelDigger as Excel
import Bot as Bot
import hero as hero
#kurwa mamy to


class Przedmioty():
    dane = []

    def __init__(self, kurwa):
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
        self.penetracja = penetracja

    def rzut_na_obrazenia(self):
        return Bot.roll_dice_from_text(self.kosc_obrazen)

    def zadaj_obrazenia(self, cel):
        cel.rana(self.rzut_na_obrazenia(), self.penetracja)

    def test_trafenia(self, operator, cel):
        if (operator.rzut_na_umiejetnasc(self.rodzaj_testu) + self.premia) >= cel.unik:
            self.zadaj_obrazenia(cel)
            return True
        else:
            return False

    def atakuj(self, operator, cel):
        return self.test_trafenia(operator, cel)


'''
itemki = Przedmioty()
m4ka = itemki.luskaczBroni("M4A1")
print(m4ka[6])
'''
