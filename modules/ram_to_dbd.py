import sqlite3
from db.dbd_const import SQL_DBD_Init


class RAMtoDBD:
    def __init__(self, ram, db_name):
        self.ram = ram
        self.connection = sqlite3.connect(db_name)

    def schema(self):
        self.connection.cursor().execute("insert into dbd$schemas (name) values(?)", (self.ram.name,))

    def tables(self):
        cursor = self.connection.cursor()
        cursor.executemany(
            """insert into dbd$tables (schema_id, name, description,
                                        can_add, can_edit, can_delete,
                                        temporal_mode, means)
                values (?, ?, ?, ?, ?, ?, ?, ?)""", list((cursor.execute(
                """select id from dbd$schemas where dbd$schemas.name = ?""", (table.schema,)).fetchone()[0],
                    table.name, table.description,
                    table.add, table.edit, table.delete,
                    table.temporal_mode, table.means
                ) for table in self.ram.tables))

    def domains(self):
        cursor = self.connection.cursor()
        cursor.executemany(
            """insert into dbd$domains (name, description, length, char_length, precision, scale, width,
                                        align, show_null, show_lead_nulls, thousands_separator, 
                                        summable, case_sensitive, data_type_id)
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", list((
                    domain.name, domain.description, domain.length, domain.char_length, domain.precision,
                    domain.scale, domain.width, domain.align, domain.show_null, domain.show_lead_nulls,
                    domain.thousands_separator, domain.summable, domain.case_sensitive, "?"
                ) for domain in self.ram.domains))
        cursor.execute(
            "create table dbd$dt (name varchar not null, type varchar not null, type_id)")
        cursor.executemany(
            "insert into dbd$dt values (?, ?, ?)", list((domain.name, domain.type, "?") for domain in self.ram.domains))
        cursor.execute(
            """update dbd$dt set type_id = (
            select id from dbd$data_types where dbd$dt.type = dbd$data_types.type_id);""")
        cursor.execute(
            """update dbd$domains set data_type_id = (
        select type_id from dbd$dt where dbd$dt.name = dbd$domains.name);""")
        cursor.execute("drop table dbd$dt")

    def fields(self):
        cursor = self.connection.cursor()
        for table in self.ram.tables:
            if table.fields:
                for field in table.fields:
                    cursor.execute(
                        """insert into dbd$fields (table_id, position, name, russian_short_name, description,
                                                    domain_id, can_input, can_edit, show_in_grid, show_in_details,
                                                    is_mean, autocalculated, required)
                    values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
                            cursor.execute(
                                """select id from dbd$tables
                            where dbd$tables.name = ?""", (table.name,)).fetchone()[0],
                            field.position, field.name, field.rname, field.description,
                            cursor.execute(
                                """select id from dbd$domains where dbd$domains.name = ?""",
                                (field.domain,)).fetchone()[0],
                            field.input, field.edit, field.show_in_grid, field.show_in_details,
                            field.is_mean, field.autocalculated, field.required))

    def constraints(self):
        cursor = self.connection.cursor()
        for table in self.ram.tables:
            if table.constraints:
                for constraint in table.constraints:
                    tid = cursor.execute("""select id from dbd$tables where dbd$tables.name = ?""",
                                         (table.name,)).fetchone()[0]
                    cursor.execute(
                        """insert into dbd$constraints (table_id, name, constraint_type, reference,
                                                        unique_key_id, has_value_edit, cascading_delete, expression)
                    values (?, ?, ?, ?, ?, ?, ?, ?)""", (
                            tid, constraint.name, constraint.kind,
                            None if constraint.reference is None else cursor.execute("""select id from dbd$tables
                             where dbd$tables.name = ?""", (constraint.reference, )).fetchone()[0],
                            constraint.unique_key_id, constraint.has_value_edit,
                            constraint.cascading_delete, constraint.expression))

    def indices(self):
        cursor = self.connection.cursor()
        for table in self.ram.tables:
            if table.indices:
                for index in table.indices:
                    kind = None
                    if not (index.fulltext ^ index.uniqueness):
                        if index.fulltext:
                            kind = "fulltext"
                        if index.uniqueness:
                            kind = "uniqueness"
                    cursor.execute(
                        """insert into dbd$indices (table_id, name, local, kind)
                    values (?, ?, ?, ?)""", (
                            cursor.execute(
                                """select id from dbd$tables
                            where dbd$tables.name = ?""", (table.name,)).fetchone()[0],
                            index.name, index.local, kind))

    def constraint_details(self):
        constraint_id = 0
        cursor = self.connection.cursor()
        for table in self.ram.tables:
            for constraint in table.constraints:
                constraint_id += 1
                cursor.execute(
                    """insert into dbd$constraint_details (constraint_id, position, field_id)
                values (?, ?, ?)""", (
                        constraint_id, 1,
                        cursor.execute(
                            """select id from dbd$fields
                        where dbd$fields.name = ?""", (constraint.items,)).fetchone()[0]))

    def index_details(self):
        index_id = 0
        cursor = self.connection.cursor()
        for table in self.ram.tables:
            for index in table.indices:
                index_id += 1
                cursor.execute(
                    """insert into dbd$index_details (index_id, position, field_id, expression, descend)
                values (?, ?, ?, ?, ?)""", (
                        index_id, 1, cursor.execute(
                            """select id from dbd$fields
                        where dbd$fields.name = ?""", (index.field,)).fetchone()[0],
                        None, None))

    def ram_to_dbd(self):
        self.connection.cursor().executescript(SQL_DBD_Init)
        self.schema()
        self.tables()
        self.domains()
        self.fields()
        self.constraints()
        self.indices()
        self.constraint_details()
        self.index_details()
        self.connection.commit()
        self.connection.close()
