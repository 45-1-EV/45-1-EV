import os
import xml.dom.minidom as dom
from modules.xml_to_ram import XMLtoRAM
from modules.ram_to_dbd import RAMToDBD

xml = dom.parse(os.path.join("xml/", "xml_test.xml"))
ram = XMLtoRAM(xml).xml_to_ram()
dbd = RAMToDBD(ram, "test.db").ram_to_dbd()
