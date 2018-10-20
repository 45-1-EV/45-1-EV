import os
import xml.dom.minidom as dom
from modules.xml_to_ram import XMLtoRAM
from modules.ram_to_dbd import RAMtoDBD
from modules.dbd_to_ram import DBDtoRAM

xml = dom.parse(os.path.join("xml/", "xml_test.xml"))
ram = XMLtoRAM(xml).xml_to_ram()
RAMtoDBD(ram, "test.db").ram_to_dbd()
ram2 = DBDtoRAM("test.db").schema()
if os.path.exists("test.db"):
    os.remove("test.db")

for d in ram2.domains:
    print(d.name)
