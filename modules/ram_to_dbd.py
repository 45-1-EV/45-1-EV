import sqlite3


class RAMToDBD:
    def __init__(self, ram, db_name):
        self.ram = ram
        self.connection = sqlite3.connect(db_name)

    def ram_to_dbd(self):
        #code
        self.connection.commit()
        self.connection.close()

