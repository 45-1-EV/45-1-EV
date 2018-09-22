import os
import xml.dom.minidom as md
from XMLtoRAM import XMLtoRAM

xml = md.parse(os.path.join("source_xml/", "xml-test.xml"))
schema = XMLtoRAM(xml).xml_to_ram()

print("----------Schema----------")
print("version= ", schema.version)
print("name= ", schema.name)
print("description= ", schema.description)

print("----------Tables----------")
for table in schema.tables:
    print("  *--", table.name, "--*")
    print("    description= ", table.description)
    for field in table.fields:
        print("    %----", field.name, "----%")
        print("      rname= ", field.rname)
        print("      domain= ", field.domain)

    print("  *---------------*")

