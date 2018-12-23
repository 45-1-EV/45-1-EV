import pyodbc
server = 'IDEA-PC\SQLEXPRESS'
database = 'Test'
user = 'sa'
password = '123'
driver = '{SQL Server}'
con = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+user+';PWD=' + password)
cursor = con.cursor()
cursor.execute("select * from Table_1")
row = cursor.fetchall()
print(row)
con.close()
