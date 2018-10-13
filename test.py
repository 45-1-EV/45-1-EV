import os
import xml.dom.minidom as dom
import sqlite3 as db
from modules.xml_to_ram import XMLtoRAM
from modules.ram_to_dbd import RAMToDBD

xml = dom.parse(os.path.join("xml/", "xml_test.xml"))
ram = XMLtoRAM(xml).xml_to_ram()
RAMToDBD(ram, "test.db").ram_to_dbd()

db = db.connect("test.db")
cursor = db.cursor()
go = '1'
while go == '1':
    print('type?')
    c = input()
    if c == 'schemas' or c == 'domains' or c == 'tables' or c == 'fields' or c == 'constraints' or c == 'indices':
        c = 'select * from dbd$'+c
        cursor.execute(c)
        t = cursor.fetchall()
        for tt in t:
            print(tt)
    print('next?')
    go = input()
db.close()
os.remove("test.db")
