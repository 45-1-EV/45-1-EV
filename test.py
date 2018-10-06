import os
import xml.dom.minidom as dom
import sqlite3 as db
from modules.xml_to_ram import XMLtoRAM
from modules.ram_to_dbd import RAMToDBD

xml = dom.parse(os.path.join("xml/", "xml_test.xml"))
ram = XMLtoRAM(xml).xml_to_ram()
dbd = RAMToDBD(ram, "test.db").ram_to_dbd()

db = db.connect("test.db")
cursor = db.cursor()
cursor.execute('select * from dbd$tables')
t = cursor.fetchall()
for tt in t:
    print(tt)
db.close()
os.remove("test.db")
