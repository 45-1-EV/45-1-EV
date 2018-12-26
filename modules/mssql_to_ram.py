import pyodbc
from db import db_classes as dbc


class MSSQLtoRAM:

    def __init__(self, database):
        self.database = database
        server = 'IDEA-PC\SQLEXPRESS'
        user = 'sa'
        password = '123'
        driver = '{SQL Server}'
        self.con = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + self.database
                                  + ';UID=' + user + ';PWD=' + password)

    def create_schema(self):
        schema = dbc.Schema()
        schema.name = self.database
        schema.description = self.database + " database from MS SQL EXPRESS"
        self.create_tables(schema)
        return schema

    def create_tables(self, schema):
        cursor = self.con.cursor()
        cursor.execute("select TABLE_NAME from INFORMATION_SCHEMA.TABLES where TABLE_TYPE='BASE TABLE'")
        tables = cursor.fetchall()
        for table in tables:
            t = dbc.Table()
            t.name = table[0]
            self.create_fields(t)
            self.create_indexes(t)
            self.create_constraints(t)
            schema.tables.append(t)
        cursor.close()

    def create_fields(self, table):
        cursor = self.con.cursor()
        cursor.execute("select COLUMN_NAME, IS_NULLABLE, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, NUMERIC_PRECISION, "
                       "NUMERIC_SCALE from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='" + table.name + "'")
        fields = cursor.fetchall()
        for field in fields:
            f = dbc.Field()
            f.name = field[0]
            f.type = field[2]
            if field[1] == 'YES':
                f.not_null = True
            if field[3] is not None:
                f.length = field[3]
            if field[4] is not None:
                f.length = field[4]
            if field[5] is not None:
                f.precision = field[5]
            table.fields.append(f)
        cursor.close()

    def create_indexes(self, table):
        cursor = self.con.cursor()
        cursor.execute("SELECT i.Name,c.Name,i.is_unique FROM sys.indexes i "
                       "INNER JOIN sys.index_columns ic ON i.index_id = ic.index_id AND i.object_id = ic.object_id "
                       "INNER JOIN sys.columns c ON ic.column_id = c.column_id AND ic.object_id = c.object_id "
                       "WHERE OBJECT_NAME(i.object_ID)='" + table.name + "'")
        indexes = cursor.fetchall()
        for index in indexes:
            ii = dbc.Index()
            ii.name = index[0]
            ii.field = index[1]
            if index[2] == 1:
                ii.uniqueness = True
            table.indices.append(ii)
        cursor.close()

    def create_constraints_primary(self, table):
        cursor = self.con.cursor()
        cursor.execute("select K.CONSTRAINT_NAME, K.COLUMN_NAME from INFORMATION_SCHEMA.KEY_COLUMN_USAGE K "
                       "INNER JOIN INFORMATION_SCHEMA.TABLE_CONSTRAINTS T ON K.CONSTRAINT_NAME=T.CONSTRAINT_NAME "
                       "WHERE T.CONSTRAINT_TYPE='PRIMARY KEY' AND K.TABLE_NAME='"+table.name+"'")
        constraints = cursor.fetchall()
        for constraint in constraints:
            c = dbc.Constraint()
            c.name = constraint[0]
            c.items = constraint[1]
            c.kind = "PRIMARY"
            table.constraints.append(c)
        cursor.close()

    def create_constraints_check(self, table):
        cursor = self.con.cursor()
        cursor.execute("select K.CONSTRAINT_NAME, K.CHECK_CLAUSE from INFORMATION_SCHEMA.CHECK_CONSTRAINTS K "
                       "INNER JOIN INFORMATION_SCHEMA.TABLE_CONSTRAINTS T ON K.CONSTRAINT_NAME=T.CONSTRAINT_NAME "
                       "WHERE T.CONSTRAINT_TYPE='CHECK' AND T.TABLE_NAME='"+table.name+"'")
        constraints = cursor.fetchall()
        for constraint in constraints:
                c = dbc.Constraint()
                c.name = constraint[0]
                c.expression = constraint[1]
                c.kind = "CHECK"
                table.constraints.append(c)
        cursor.close()

    def create_constraints_unique(self, table):
        cursor = self.con.cursor()
        cursor.execute("select K.CONSTRAINT_NAME, K.COLUMN_NAME from INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE  K "
                       "INNER JOIN INFORMATION_SCHEMA.TABLE_CONSTRAINTS T ON K.CONSTRAINT_NAME=T.CONSTRAINT_NAME "
                       "WHERE T.CONSTRAINT_TYPE='UNIQUE' AND T.TABLE_NAME='"+table.name+"'")
        constraints = cursor.fetchall()
        for constraint in constraints:
                c = dbc.Constraint()
                c.name = constraint[0]
                c.items = constraint[1]
                c.kind = "UNIQUE"
                table.constraints.append(c)
        cursor.close()

    def create_constraints_foreign(self, table):
        cursor = self.con.cursor()
        cursor.execute("SELECT fk.name, c1.name, OBJECT_NAME(fk.referenced_object_id), c2.name "
                       "FROM sys.foreign_keys fk INNER JOIN "
                       "sys.foreign_key_columns fkc ON fkc.constraint_object_id = fk.object_id INNER JOIN "
                       "sys.columns c1 ON fkc.parent_column_id = c1.column_id AND fkc.parent_object_id = c1.object_id "
                       "INNER JOIN sys.columns c2 ON fkc.referenced_column_id = c2.column_id "
                       "AND fkc.referenced_object_id = c2.object_id "
                       "WHERE OBJECT_NAME(fk.parent_object_id)='"+table.name+"'")
        constraints = cursor.fetchall()
        for constraint in constraints:
                c = dbc.Constraint()
                c.name = constraint[0]
                c.items = constraint[1]
                c.reference = constraint[2]
                c.ref_field = constraint[3]
                c.kind = "FOREIGN"
                table.constraints.append(c)
        cursor.close()

    def create_constraints(self, table):
        self.create_constraints_primary(table)
        self.create_constraints_check(table)
        self.create_constraints_unique(table)
        self.create_constraints_foreign(table)
