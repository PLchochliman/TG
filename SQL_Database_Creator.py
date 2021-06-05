#import psycopg2
import FilesMenagment as FilesMenagment
import excelDigger as excel
import SQL_Base_Handling as SQL

def log_and_load_database(auth):
    conn = SQL.establish_connection_with_base("postgres", auth)
    cursor = conn.cursor()

    try:
       cursor.execute('''DROP DATABASE tg;''')
    except Exception:
       print("there were no DataBase")

    cursor.execute('CREATE DATABASE tg;')

    conn = SQL.establish_connection_with_base("tg", auth)
    cursor = conn.cursor()
    print("Database created and connected successfully........")

    #SQL.table_creator("bron", ["Nazwa varchar(128)", "Premia int"], cursor)
    nazwy_tabel = ['bron', 'bronbiala', 'granaty', 'celowniki', 'amunicja', 'dodatki',
                                                    'szpej', 'plyty_balistyczne', 'tarcze', 'apteczki',
                                                    'radia_i_komunikacja', 'jedzenie',  'zestawy_dajace_premie',
                                                    'drobnica', 'gotowe_zestawy']
    zasieg_danych = ['O232', 'I20', 'I10', 'I25', 'I36', 'H5', 'I40', 'G9', 'G4', 'G11', 'H10', 'F7', 'D6', 'D37', 'D6']

    przetwornik = excel.Loader('TabelaBroni.xlsx', nazwy_tabel, zasieg_danych)
    dane = przetwornik.zwroc()
    przetwornik.wyczysc()

    for table in range(0, len(dane)):
       SQL.convert_excel_into_table(nazwy_tabel[table], dane[table], cursor)
    return conn


def test():
    auth = FilesMenagment.OtworzPlik("LogiDoBazy.env") # to this file enter name of database, and password in second line
    log_and_load_database(auth)    #to update just uncomment this line
    conn = SQL.establish_connection_with_base("tg", auth)
    cursor = conn.cursor()

    #cursor.execute('select * FROM bron')
    #print(cursor.fetchall())
    #
    #print(SQL.get_item_from_table("m4a1", 'bron', cursor))

    conn.close()

#test()