#import psycopg2
import FilesMenagment as FilesMenagment
import excelDigger as excel
import SQL_Base_Handling as SQL

auth = FilesMenagment.OtworzPlik("LogiDoBazy.env") # to this file enter name of database, and password in second line
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

cursor.execute(SQL.table_creator("bron", ["Nazwa varchar(128)", "Premia int"]))

print("Table created successfully........")












conn.close()
