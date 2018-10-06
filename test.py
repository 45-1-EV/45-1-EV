import os
import xml.dom.minidom as dom
from modules.xml_to_ram import XMLtoRAM

xml = dom.parse(os.path.join("xml/", "xml_test.xml"))
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
    for con in table.constraints:
        print("    %----constraint----%")
        print("      kind= ", con.kind)
        print("      items= ", con.items)
    for ind in table.indices:
        print("    %----index----%")
        print("      field= ", ind.field)

    print("  *---------------*")

