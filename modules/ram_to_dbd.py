import sqlite3
from db.dbd_const import SQL_DBD_Init


class RAMToDBD:
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
                values (?, ?, ?, ?, ?, ?, ?, ?)""", list((
                    1, table.name, table.description,
                    table.add, table.edit, table.delete,
                    table.temporal_mode, table.means
                ) for table in self.ram.tables))

    def ram_to_dbd(self):
        self.connection.cursor().executescript(SQL_DBD_Init)
        self.schema()
        self.tables()
        self.connection.commit()
        self.connection.close()
