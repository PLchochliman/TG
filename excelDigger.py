import Bot
import pylightxl as xl


class Loader: #pelne pokrycie
    sorowka = []
    zaladowane = []

    """
    makes basic load xlsx file from system.
    """

    def __init__(self, nazwa, arkusz, zasieg):
        self.sorowka = xl.readxl(fn=nazwa)
        self.zaladowane = []
        for i in range(0, len(arkusz)):
            self.zaladowane.append(self.zaladuj_arkusz(arkusz[i], zasieg[i]))
        self.sorowka = []

    """
    loads the sheet from document (you provide name, and end cell)
    """

    def zaladuj_arkusz(self, arkusz, zasieg):
        return self.sorowka.ws(ws=arkusz).range(address='A1:'+zasieg, formula=False)

    """
    returns to user table, as table, where alll words are made to lower.
    """

    def zwroc(self):
        for i in range(0, len(self.zaladowane)):
            for y in range(0, len(self.zaladowane[i])):
                for z in range(0, len(self.zaladowane[i][y])):
                    if isinstance(self.zaladowane[i][y][z], str):
                        self.zaladowane[i][y][z] = self.zaladowane[i][y][z].lower()
        return self.zaladowane

    """
    clears the loading - it did some bugs previously.
    """

    def wyczysc(self):
        self.zaladowane = []


#giweryICelowniki = Loader('TabelaBroni.xlsx', ['bron', 'bronbiala', 'granaty', 'lunety', 'celowniki',], ['O300', 'I19','I10', 'F13', 'G14'])
#print(giweryICelowniki.zwroc())
