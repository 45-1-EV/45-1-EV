import db_classes as dbc


class XMLtoRAM:
    def __init__(self, xml_file):
        self.xml_repr = xml_file
        self.tables_list = self.get_tables()

    def xml_to_ram(self):
        return self.get_schema()

    def get_domains(self):
        domain_list = list()
        for domain in self.xml_repr.getElementsByTagName("domain"):
            dom = dbc.Domain()
            for an, av in domain.attributes.items():
                if an.lower() == "name":
                    dom.name = av
                elif an.lower() == "description":
                    dom.description = av
                elif an.lower() == "type":
                    dom.type = av
                elif an.lower() == "align":
                    dom.align = av
                elif an.lower() == "width":
                    dom.width = av
                elif an.lower() == "props":
                    for prop in av.split(", "):
                        if prop == "show_null":
                            dom.show_null = True
                        elif prop == "summable":
                            dom.summable = True
                        elif prop == "case_sensitive":
                            dom.case_sensitive = True
                        elif prop == "show_lead_nulls":
                            dom.show_lead_nulls = True
                        elif prop == "thousand_separator":
                            dom.thousands_separator = True
                elif an.lower() == "char_length":
                    dom.char_length = av
                elif an.lower() == "length":
                    dom.length = av
                elif an.lower() == "precision":
                    dom.precision = av
                elif an.lower() == "scale":
                    dom.scale = av
            domain_list.append(dom)

        return domain_list

    @staticmethod
    def get_indices(table):
        indices_list = list()
        for index in table.getElementsByTagName("index"):
            idx = dbc.Index()
            for an, av in index.attributes.items():
                if an.lower() == "name":
                    idx.name = av
                elif an.lower() == "field":
                    idx.field = av
                elif an.lower() == "props":
                    for prop in av.split(", "):
                        if prop == "fulltext":
                            idx.fulltext = True
                        elif prop == "uniqueness":
                            idx.uniqueness = True
                        elif prop == "local":
                            idx.local = True
            indices_list.append(idx)

        return indices_list

    @staticmethod
    def get_constraints(table):
        constraints_list = list()
        for constraint in table.getElementsByTagName("constraint"):
            const = dbc.Constraint()
            for an, av in constraint.attributes.items():
                if an.lower() == "name":
                    const.name = av
                elif an.lower() == "kind":
                    const.kind = av
                elif an.lower() == "items":
                    const.items = av
                elif an.lower() == "unique_key_id":
                    const.unique_key_id = av
                elif an.lower() == "reference":
                    const.reference = av
                elif an.lower() == "expression":
                    const.expression = av
                elif an.lower() == "props":
                    for prop in av.split(", "):
                        if prop == "has_value_edit":
                            const.has_value_edit = True
                        elif prop == "cascading_delete":
                            const.cascading_delete = True
            constraints_list.append(const)

        return constraints_list

    @staticmethod
    def get_fields(table):
        fields_list = list()
        pos = 1
        for field in table.getElementsByTagName("field"):
            fld = dbc.Field()
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
            tbl = dbc.Table()
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
            tbl.indices = self.get_indices(table)
            tbl.constraints = self.get_constraints(table)
            tables_list.append(tbl)

        return tables_list

    def get_schema(self):
        schema = dbc.Schema()

        for an, av in self.xml_repr.documentElement.attributes.items():
            if an.lower() == "version":
                schema.version = av
            elif an.lower() == "name":
                schema.name = av
            elif an.lower() == "description":
                schema.description = av
        schema.tables = self.tables_list

        return schema

