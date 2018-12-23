from modules.post_ddl import PostDDL
from modules.xml_to_ram import XMLtoRAM
import xml.dom.minidom as dom
import psycopg2
import os

dbname = "Test"
usr = "postgres"
pasw = "123"

for t in ["tasks", "prjadm"]:
    xml_file = os.path.join("xml/", t+".xml")
    xml = dom.parse(xml_file)
    ram = XMLtoRAM(xml).xml_to_ram()

    conn = psycopg2.connect("dbname=" + dbname + " user=" + usr + " password=" + pasw)
    DDL = PostDDL(ram, usr).filling_db()
    cur = conn.cursor()
    cur.execute(DDL)
    cur.close()
    conn.commit()
    conn.close()

    f = open("post_ddl_"+t+".txt", "w")
    f.write(DDL)
