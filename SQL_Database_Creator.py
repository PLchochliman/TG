import psycopg2
import FilesMenagment as FilesMenagment




auth = FilesMenagment.OtworzPlik("LogiDoBazy.env") #to this file enter name of database, and password in second line

#establishing the connection
conn = psycopg2.connect(
   database="postgres", user=auth[0], password=auth[1], host='127.0.0.1', port='5432'
)
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Preparing query to create a database
sql = '''DROP database TG''';

#Creating a database
cursor.execute(sql)

#Preparing query to create a database
sql = '''CREATE database TG''';

#Creating a database
cursor.execute(sql)
print("Database created successfully........")

#Closing the connection
conn.close()
