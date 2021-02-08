import Bot
import pylightxl as xl


class loader():
    sorowka = []
    zaladowane = []

    def __init__(self, nazwa, arkusz, zasieg ):
        self.sorowka = xl.readxl(fn=nazwa)
        for i in range(0, len(arkusz)):
            self.zaladowane.append(self.zaladujArkusz(arkusz[i], zasieg[i]))

    def zaladujArkusz(self, arkusz, zasieg):
        return self.sorowka.ws(ws=arkusz).range(address='A1:'+zasieg, formula=False)

    def zwroc(self):
        return self.zaladowane


#giweryICelowniki = loader('TabelaBroni.xlsx', ['bron', 'bronbiala', 'granaty', 'lunety', 'celowniki',], ['O300', 'I19','I10', 'F13', 'G14'])
#print(giweryICelowniki.zwroc())
