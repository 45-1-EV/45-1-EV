import sqlite3
from db.dbd_const import SQL_DBD_Init


class RAMToDBD:
    def __init__(self, ram, db_name):
        self.ram = ram
        self.connection = sqlite3.connect(db_name)

    def ram_to_dbd(self):
        self.connection.cursor().executescript(SQL_DBD_Init)
        #code
        self.connection.commit()
        self.connection.close()

