import excelDigger as Excel


class Przedmioty(): #pełne pokrycie
    dane = []

    """
    loads the guns, and accesories to TG from file
    """

    def __init__(self):
        self.przetwornik = \
            Excel.Loader('TabelaBroni.xlsx', ['bron', 'bronbiala', 'granaty', 'celowniki', 'amunicja', 'dodatki',
                         'szpej', 'plyty_balistyczne', 'tarcze', 'apteczki', 'radia_i_komunikacja', 'jedzenie',
                         'zestawy_dajace_premie', 'drobnica', 'gotowe_zestawy', 'mundury'],
                         ['O232', 'I20', 'I10', 'I25', 'I36', 'H5', 'I40', 'G9', 'G4', 'G11', 'H10', 'F7', 'D6', 'D37',
                         'D6', 'F8'])
        self.dane = self.przetwornik.zwroc()
        self.przetwornik.wyczysc()

    """
    Enable to select single gun
    """

    def luskacz_broni(self, nazwaBroni):
        for i in self.dane[0]:
            if i[0] == nazwaBroni:
                return i
        return False

    """
    enable to select single melee weapon
    """

    def luskacz_broni_bialej(self, nazwaBroni):
        for i in self.dane[1]:
            if i[0] == nazwaBroni:
                return i
        return False

    """
    enable to select single granade
    """

    def luskacz_granatow(self, nazwaBroni):
        for i in self.dane[2]:
            if i[0] == nazwaBroni:
                return i
        return False

    """
    enables to select single scope
    """

    def luskacz_celownikow(self, nazwaBroni):
        for i in self.dane[3]:
            if i[0] == nazwaBroni:
                return i
        return False

    """
    enable to select ammunition
    """

    def luskacz_amunicji(self, nazwa_amunicji):
        for i in self.dane[4]:
            if i[0] == nazwa_amunicji:
                return i
        return False

    def luskacz_dodatkow(self, nazwa_dodatku):
        for i in self.dane[5]:
            if i[0] == nazwa_dodatku:
                return i
        return False

    def wyszukaj_przedmiot_i_zwroc_po_wszystkim(self, nazwa):
        for tabela in self.dane:
            for rekord in tabela:
                if rekord[0] == nazwa:
                    return rekord
        return False

    def wyszukaj_przedmiot_i_zwroc_po_wszystkim_z_nazwa_tabeli(self, nazwa):
        for tabela in self.dane:
            for rekord in tabela:
                if rekord[0] == nazwa:
                    return [rekord, tabela]
        return False
