import psycopg2

def table_creator(nazwa_tabeli, lista_kolumn_z_typami, cursor): #first column will be Primary Key
   # lista_kolumn z typami should look:var type eg name varchar(128)
   komenda_tworzenia_tabeli = "CREATE TABLE " + nazwa_tabeli + " (\n"
   for i in range(0, len(lista_kolumn_z_typami)):
      if i == 0:
         komenda_tworzenia_tabeli = "\t" + komenda_tworzenia_tabeli + lista_kolumn_z_typami[i] + " PRIMARY KEY,\n"
      elif i == len(lista_kolumn_z_typami) - 1:
         komenda_tworzenia_tabeli = "\t" + komenda_tworzenia_tabeli + lista_kolumn_z_typami[i] + "\n"
      else:
         komenda_tworzenia_tabeli = "\t" + komenda_tworzenia_tabeli + lista_kolumn_z_typami[i] + ",\n"
   komenda_tworzenia_tabeli = komenda_tworzenia_tabeli + ");"
   print(komenda_tworzenia_tabeli)
   cursor.execute(komenda_tworzenia_tabeli)
   return True


def establish_connection_with_base(name_of_base, auth):
   conn = psycopg2.connect(
      database=name_of_base, user=auth[0], password=auth[1], host='127.0.0.1', port='5432'  # settings are default.
   )
   conn.autocommit = True
   return conn


def is_a_number(s):
   try:
      float(s)
      return True
   except ValueError:
      return False


def convert_excel_into_table(name, table, conn):
   table_of_headers_with_variables = []
   headers = table[0]
   typeof = table[1]
   for iterator in range(0, len(headers)):
      if is_a_number(typeof[iterator]):
         table_of_headers_with_variables.append((headers[iterator] + " " + "float"))
      else:
         table_of_headers_with_variables.append((headers[iterator] + " " + "varchar(128)"))
   table_creator(name, table_of_headers_with_variables, conn)
   return True