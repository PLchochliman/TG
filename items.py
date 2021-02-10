import excelDigger as excel
#kurwa mamy to


class Przedmioty():
    dane = []

    def __init__(self, kurwa):
        self.przetwornik = excel.loader('TabelaBroni.xlsx', ['bron', 'bronbiala', 'granaty', 'lunety', 'celowniki'],
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


'''
itemki = Przedmioty()
m4ka = itemki.luskaczBroni("M4A1")
print(m4ka[6])
'''
