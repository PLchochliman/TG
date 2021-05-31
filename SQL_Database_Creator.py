#import psycopg2
import FilesMenagment as FilesMenagment
import excelDigger as excel
import SQL_Base_Handling as SQL

def log_and_load_database(auth):
    conn = SQL.establish_connection_with_base("postgres", auth)
    cursor = conn.cursor()

    try:
       cursor.execute('''DROP DATABASE tg;''')
       #cursor.execute('''DROP TABLE bron;''')
    except Exception:
       print("there were no DataBase")

    cursor.execute('CREATE DATABASE tg;')

    conn = SQL.establish_connection_with_base("tg", auth)
    cursor = conn.cursor()
    print("Database created and connected successfully........")

    #SQL.table_creator("bron", ["Nazwa varchar(128)", "Premia int"], cursor)

    przetwornik = excel.Loader('TabelaBroni.xlsx', ['bron', 'bronbiala', 'granaty', 'celowniki', 'amunicja', 'dodatki'],
                               ['O300', 'I19', 'I10', 'I28', 'I42', 'H5'])
    dane = przetwornik.zwroc()
    przetwornik.wyczysc()

    nazwy = ['bron', 'bronbiala', 'granaty', 'celowniki', 'amunicja', 'dodatki']
    for table in range(0,len(dane)):
       SQL.convert_excel_into_table(nazwy[table], dane[table], cursor)
    return conn

auth = FilesMenagment.OtworzPlik("LogiDoBazy.env") # to this file enter name of database, and password in second line

#conn = log_and_load_database(auth)
conn = SQL.establish_connection_with_base("tg", auth)
cursor = conn.cursor()
print("Tables created successfully........")

print(SQL.get_item_from_table("acogx3", 'celowniki', cursor))







conn.close()
