import os
import io
import codecs
import difflib
import xml.dom.minidom as dom
from modules.xml_to_ram import XMLtoRAM
from modules.ram_to_dbd import RAMtoDBD
from modules.dbd_to_ram import DBDtoRAM
from modules.ram_to_xml import RAMtoXML

if os.path.exists("diff_error.html"):
    os.remove("diff_error.html")
for t in ["tasks", "prjadm"]:
    if os.path.exists("test.xml"):
        os.remove("test.xml")
    if os.path.exists("test.db"):
        os.remove("test.db")
    if os.path.exists("diff_"+t+".html"):
        os.remove("diff_"+t+".html")

    xml_file = os.path.join("xml/", t+".xml")

    xml = dom.parse(xml_file)
    ram = XMLtoRAM(xml).xml_to_ram()
    RAMtoDBD(ram, "test.db").ram_to_dbd()
    ram2 = DBDtoRAM("test.db").dbd_to_ram()
    xml2 = RAMtoXML(ram2).ram_to_xml()

    with open("test.xml", "wb") as f:
        f.write(xml2.toprettyxml(encoding="utf-8", indent="  "))

    text1 = io.open(xml_file, encoding='utf-8').readlines()
    text2 = io.open("test.xml", encoding='utf-8').readlines()
    d = difflib.HtmlDiff()
    html = d.make_file(text1, text2)
    file = codecs.open("diff_"+t+".html", 'w', 'utf-8')
    file.write(html)
    file.close()
# make fake error file
for table in ram2.tables:
    for field in table.fields:
        field.name = "error"
xml2 = RAMtoXML(ram2).ram_to_xml()
with open("test.xml", "wb") as f:
    f.write(xml2.toprettyxml(encoding="utf-8", indent="  "))
text1 = io.open(xml_file, encoding='utf-8').readlines()
text2 = io.open("test.xml", encoding='utf-8').readlines()
d = difflib.HtmlDiff()
html = d.make_file(text1, text2)
file = codecs.open("diff_error.html", 'w', 'utf-8')
file.write(html)
file.close()
