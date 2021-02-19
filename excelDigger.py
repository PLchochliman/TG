import Bot
import pylightxl as xl


class Loader(): #pelne pokrycie
    sorowka = []
    zaladowane = []

    def __init__(self, nazwa, arkusz, zasieg):
        self.sorowka = xl.readxl(fn=nazwa)
        for i in range(0, len(arkusz)):
            self.zaladowane.append(self.zaladuj_arkusz(arkusz[i], zasieg[i]))

    def zaladuj_arkusz(self, arkusz, zasieg):
        return self.sorowka.ws(ws=arkusz).range(address='A1:'+zasieg, formula=False)

    def zwroc(self):
        for i in range(0, len(self.zaladowane)):
            for y in range(0, len(self.zaladowane[i])):
                for z in range(0, len(self.zaladowane[i][y])):
                    if isinstance(self.zaladowane[i][y][z], str):
                        self.zaladowane[i][y][z] = self.zaladowane[i][y][z].lower()
        return self.zaladowane


#giweryICelowniki = Loader('TabelaBroni.xlsx', ['bron', 'bronbiala', 'granaty', 'lunety', 'celowniki',], ['O300', 'I19','I10', 'F13', 'G14'])
#print(giweryICelowniki.zwroc())
