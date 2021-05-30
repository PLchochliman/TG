import psycopg2
import FilesMenagment as FilesMenagment


def SQL_table_creator(nazwa_tabeli, lista_kolumn_z_typami): #first column will be Primary Key
   # lista_kolumn z typami should look:var type eg name varchar(128)
   komenda_tworzenia_tabeli = "CREATE TABLE " + nazwa_tabeli + " (\n"
   for i in range(0, len(lista_kolumn_z_typami)):
      if i == 0:
         komenda_tworzenia_tabeli = "\t" + komenda_tworzenia_tabeli + lista_kolumn_z_typami[i] + " PRIMARY KEY,\n"
      elif i == len(lista_kolumn_z_typami):
         komenda_tworzenia_tabeli = "\t" + komenda_tworzenia_tabeli + lista_kolumn_z_typami[i] + ",\n"
      else:
         komenda_tworzenia_tabeli = "\t" + komenda_tworzenia_tabeli + lista_kolumn_z_typami[i] + "\n"
   komenda_tworzenia_tabeli = komenda_tworzenia_tabeli + ");"
   return komenda_tworzenia_tabeli



auth = FilesMenagment.OtworzPlik("LogiDoBazy.env") # to this file enter name of database, and password in second line

#establishing the connection
conn = psycopg2.connect(
   database="postgres", user=auth[0], password=auth[1], host='127.0.0.1', port='5432'# settings are default.
)
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

try:
   cursor.execute('''DROP DATABASE tg;''')
   #cursor.execute('''DROP TABLE bron;''')
except Exception:
   print("there were no DataBase")

cursor.execute('CREATE DATABASE tg;')
conn = psycopg2.connect(
   database="tg", user=auth[0], password=auth[1], host='127.0.0.1', port='5432'# settings are default.
)

cursor = conn.cursor()

#cursor.execute('\\c tg')
print("Database created and connected successfully........")

cursor.execute(SQL_table_creator("bron", ["Nazwa varchar(128)", "Premia int"]))

print("Table created successfully........")


conn.close()
