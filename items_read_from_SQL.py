import SQL_Base_Handling as SQL
import FilesMenagment as FilesMenagment


class Przedmioty():
    cursor = []
    """
    loads the guns, and accesories to TG from file
    """

    def __init__(self):

        auth = FilesMenagment.OtworzPlik(
            "LogiDoBazy.env")  # to this file enter name of database, and password in second line
        #log_and_load_database(auth)    #to update just uncomment this line
        conn = SQL.establish_connection_with_base("tg", auth)
        self.cursor = conn.cursor()

        #print(SQL.get_item_from_table("acogx3", 'celowniki', cursor))

    """
    Enable to select single gun ['bron', 'bronbiala', 'granaty', 'celowniki', 'amunicja', 'dodatki']
    """

    def luskacz_broni(self, nazwa):
        return SQL.get_item_from_table(nazwa, 'bron', self.cursor)

    """
    enable to select single melee weapon
    """

    def luskacz_broni_bialej(self, nazwa):
        return SQL.get_item_from_table(nazwa, 'bronbiala', self.cursor)

    """
    enable to select single granade
    """

    def luskacz_granatow(self, nazwa):
        return SQL.get_item_from_table(nazwa, 'granaty', self.cursor)

    """
    enables to select single scope
    """

    def luskacz_celownikow(self, nazwa):
        return SQL.get_item_from_table(nazwa, 'celowniki', self.cursor)

    """
    enable to select ammunition
    """

    def luskacz_amunicji(self, nazwa_amunicji):
        return SQL.get_item_from_table(nazwa_amunicji, 'amunicja', self.cursor)

    def luskacz_dodatkow(self, nazwa_dodatku):
        return SQL.get_item_from_table(nazwa_dodatku, 'dodatki', self.cursor)

    def wyszukaj_przedmiot_i_zwroc_po_wszystkim(self, nazwa):
        for tabela in ['bron', 'bronbiala', 'granaty', 'celowniki', 'amunicja', 'dodatki']:
            return SQL.get_item_from_table(nazwa, tabela, self.cursor)
