from modules.mssql_to_ram import MSSQLtoRAM
from modules.post_ddl import PostDDL
import psycopg2

database = 'Northwind'
schema = MSSQLtoRAM(database).create_schema()

dbname = "Test"
usr = "postgres"
pasw = "123"
conn = psycopg2.connect("dbname=" + dbname + " user=" + usr + " password=" + pasw)
DDL = PostDDL(schema, usr).filling_db()
cur = conn.cursor()
cur.execute(DDL)
cur.close()
conn.commit()
conn.close()
