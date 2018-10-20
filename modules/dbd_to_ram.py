import sqlite3
import db.db_classes as dbc


class DBDtoRAM:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)

    def dbd_to_ram(self):
        return self.schema()

    def schema(self):
        cursor = self.connection.cursor()
        schema = dbc.Schema()
        schema_attributes = cursor.execute("""select name, description, version, fulltext_engine
        from dbd$schemas""").fetchall()
        for a in schema_attributes:
            schema.name, schema.description, schema.version, schema.fulltext_engine = a
        schema.domains = self.domains()
        schema.tables = self.tables()
        self.connection.commit()
        self.connection.close()
        return schema

    def domains(self):
        cursor = self.connection.cursor()
        domain_list = list()
        domain_attributes = cursor.execute("""\
          select name, description, data_type_id, align, width, length, precision, show_null, summable, case_sensitive, \
          show_lead_nulls, thousands_separator, char_length, scale from dbd$domains""").fetchall()
        for a in domain_attributes:
            domain = dbc.Domain()
            domain.name, domain.description, domain.type, domain.align, domain.width, domain.length,\
                domain.precision, domain.show_null, domain.summable, domain.case_sensitive, domain.show_lead_nulls,\
                domain.thousands_separator, domain.char_length, domain.scale = a
            domain.show_null, domain.show_lead_nulls, domain.thousands_separator, domain.summable,\
                domain.case_sensitive = map(bool, [domain.show_null, domain.show_lead_nulls, domain.thousands_separator,
                                            domain.summable, domain.case_sensitive])
            domain.char_length = str(domain.char_length) if domain.char_length else None
            domain.length = str(domain.length) if domain.length else None
            domain.scale = str(domain.scale) if domain.scale else None
            domain.precision = str(domain.precision) if domain.precision else None
            domain.width = str(domain.width) if domain.width else None
            domain.type = cursor.execute("""select type_id from dbd$data_types where dbd$data_types.id = ?""",
                                         (domain.type,)).fetchone()[0]
            domain_list.append(domain)
        return domain_list

    def fields(self, table_id):
        cursor = self.connection.cursor()
        field_list = list()
        filed_attributes = cursor.execute("""\
        select name, russian_short_name, description, domain_id, can_input, can_edit, \
        show_in_grid, show_in_details, is_mean, autocalculated, required from dbd$fields\
        where dbd$fields.table_id = ?""", (table_id,)).fetchall()
        for a in filed_attributes:
            field = dbc.Field()
            field.name, field.rname, field.description, field.domain, field.input, field.edit, \
                field.show_in_grid, field.show_in_details, field.is_mean, field.autocalculated, \
                field.required = a
            field.input, field.edit, field.show_in_grid, field.show_in_details, field.is_mean, field.autocalculated, \
                field.required = map(bool, [field.input, field.edit, field.show_in_grid, field.show_in_details,
                                            field.is_mean, field.autocalculated, field.required])
            field.domain = cursor.execute("""select name from dbd$domains where dbd$domains.id = ?""",
                                          (field.domain, )).fetchone()[0]
            field_list.append(field)
        return field_list

    def constraints(self, table_id):
            cursor = self.connection.cursor()
            constraints_list = list()
            constraints_attributes = cursor.execute("""select id, table_id, name, constraint_type, reference,\
            unique_key_id, has_value_edit, cascading_delete, expression\
            from dbd$constraints where dbd$constraints.table_id = ?""", (table_id,)).fetchall()
            for a in constraints_attributes:
                constraint = dbc.Constraint()
                i, tbl, constraint.name, constraint.kind, constraint.reference, constraint.unique_key_id, \
                    constraint.has_value_edit, constraint.cascading_delete, constraint.expression = a
                constraint.has_value_edit, constraint.cascading_delete = map(bool, [constraint.has_value_edit,
                                                                                    constraint.cascading_delete])
                constraint.items = cursor.execute("""select name from dbd$fields where dbd$fields.id = (\
                            select field_id from dbd$constraint_details\
                            where dbd$constraint_details.constraint_id = ?)""", (a[0],)).fetchone()[0]
                constraint.reference = None if constraint.kind == "PRIMARY" else cursor.execute("""\
                select name from dbd$tables where dbd$tables.id = ?""", (constraint.reference, )).fetchone()[0]
                constraints_list.append(constraint)
            return constraints_list

    def indices(self, table_id):
        cursor = self.connection.cursor()
        indices_list = list()
        indices_attributes = cursor.execute("""select id, name, local, kind from dbd$indices\
        where dbd$indices.table_id = ?""", (table_id, )).fetchall()
        for a in indices_attributes:
            index = dbc.Index()
            if a[3] == "fulltext":
                index.fulltext, index.uniqueness = True, False
            elif a[3] == "uniqueness":
                index.fulltext, index.uniqueness = False, True
            else:
                index.fulltext, index.uniqueness = False, False
            index.name, index.local = a[1:-1]
            index.field = cursor.execute("""select name from dbd$fields where dbd$fields.id = (\
            select field_id from dbd$index_details\
            where dbd$index_details.index_id = ?)""", (a[0], )).fetchone()[0]
            indices_list.append(index)
        return indices_list

    def tables(self):
        cursor = self.connection.cursor()
        tables_list = list()
        tables_attributes = cursor.execute("""\
        select id, name, description, can_add, can_edit, can_delete, temporal_mode, means from dbd$tables""").fetchall()
        for a in tables_attributes:
            table = dbc.Table()
            tid, table.name, table.description, table.add, table.edit, table.delete, table.temporal_mode, \
                table.means = a
            table.add, table.edit, table.delete = map(bool, [table.add, table.edit, table.delete])
            table.fields = self.fields(tid)
            table.constraints = self.constraints(tid)
            table.indices = self.indices(tid)
            tables_list.append(table)
        return tables_list
