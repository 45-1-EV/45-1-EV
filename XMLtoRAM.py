import Classes


class XMLtoRAM:
    def __init__(self, xml_file):
        self.xml_repr = xml_file
        self.tables_list = self.get_tables()

    def xml_to_ram(self):
        return self.get_schema()

    @staticmethod
    def get_fields(table):
        fields_list = list()
        pos = 1
        for field in table.getElementsByTagName("field"):
            fld = Classes.Field()
            fld.position = str(pos)
            for an, av in field.attributes.items():
                if an.lower() == "name":
                    fld.name = av
                elif an.lower() == "rname":
                    fld.rname = av
                elif an.lower() == "domain":
                    fld.domain = av
                elif an.lower() == "description":
                    fld.description = av
                elif an.lower() == "props":
                    for prop in av.split(", "):
                        if prop == "input":
                            fld.input = True
                        elif prop == "edit":
                            fld.edit = True
                        elif prop == "show_in_grid":
                            fld.show_in_grid = True
                        elif prop == "show_in_details":
                            fld.show_in_details = True
                        elif prop == "autocalculated":
                            fld.autocalculated = True
                        elif prop == "is_mean":
                            fld.is_mean = True
                        elif prop == "required":
                            fld.required = True
            pos += 1
            fields_list.append(fld)

        return fields_list

    def get_tables(self):
        tables_list = list()
        for table in self.xml_repr.getElementsByTagName("table"):
            tbl = Classes.Table()
            for an, av in table.attributes.items():
                if an.lower() == "name":
                    tbl.name = av
                elif an.lower() == "description":
                    tbl.description = av
                elif an.lower() == "props":
                    for prop in av.split(", "):
                        if prop == "add":
                            tbl.add = True
                        elif prop == "edit":
                            tbl.edit = True
                        elif prop == "delete":
                            tbl.delete = True
                        elif prop == "temporal_mode":
                            tbl.temporal_mode = True
                elif an.lower() == "ht_table_flags":
                    tbl.ht_table_flags = av
                elif an.lower() == "access_level":
                    tbl.access_level = av
                elif an.lower() == "means":
                    tbl.means = av

            tbl.fields = self.get_fields(table)
            tables_list.append(tbl)

        return tables_list

    def get_schema(self):
        schema = Classes.Schema()

        for an, av in self.xml_repr.documentElement.attributes.items():
            if an.lower() == "version":
                schema.version = av
            elif an.lower() == "name":
                schema.name = av
            elif an.lower() == "description":
                schema.description = av
        schema.tables = self.tables_list

        return schema

