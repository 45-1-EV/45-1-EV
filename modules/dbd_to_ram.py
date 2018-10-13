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
        schema.name = cursor.execute("""select name from dbd$schemas""").fetchone()[0]
#       schema.domains = self.domains()
#       schema.tables = self.tables()
        self.connection.commit()
        self.connection.close()
        return schema
