import psycopg2
import psycopg2.sql as psql


class PostDDL:

    def __init__(self, ram, dbname, usr, pasw):
        self.ram_repr = ram
        self.usr = usr
        self.conn = psycopg2.connect("dbname="+dbname+" user="+usr+" password="+pasw)

    def filling_db(self):
        self.create_schema()
        self.create_domains()
        self.create_tables()
        self.conn.commit()
        self.conn.close()

    def create_schema(self):
        cur = self.conn.cursor()
        req = "CREATE SCHEMA {} AUTHORIZATION "+self.usr
        cur.execute(psql.SQL(req).format(psql.Identifier(self.ram_repr.name)))
        if self.ram_repr.description:
            req = "COMMENT ON SCHEMA {} IS '"+self.ram_repr.description+"'"
            cur.execute(psql.SQL(req).format(psql.Identifier(self.ram_repr.name)))
        cur.close()

    def create_domains(self):
        cur = self.conn.cursor()
        for domain in self.ram_repr.domains:
            req = "CREATE DOMAIN "+self.ram_repr.name+".{} AS "+domain.type
            if domain.length:
                req += " ("+str(domain.length)
                if domain.precision:
                    req += ","+str(domain.precision)
                req += ")"
            if domain.not_null:
                req += " NOT NULL"
            cur.execute(psql.SQL(req).format(psql.Identifier(domain.name)))
            if domain.description:
                req = "COMMENT ON DOMAIN "+self.ram_repr.name+".{} IS '"+domain.description+"'"
                cur.execute(psql.SQL(req).format(psql.Identifier(domain.name)))
        cur.close()

    def create_tables(self):
        cur = self.conn.cursor()
        for table in self.ram_repr.tables:
            req = "CREATE TABLE "+self.ram_repr.name+".{} () WITH (OIDS = FALSE)"
            cur.execute(psql.SQL(req).format(psql.Identifier(table.name)))
            req = "ALTER TABLE "+self.ram_repr.name+".{} OWNER to "+self.usr
            cur.execute(psql.SQL(req).format(psql.Identifier(table.name)))
            if table.description:
                req = "COMMENT ON TABLE "+self.ram_repr.name+".{} IS '"+table.description+"'"
                cur.execute(psql.SQL(req).format(psql.Identifier(table.name)))
            self.create_fields(table)
            self.create_indices(table)
            self.create_constraints(table)
        cur.close()

    def create_fields(self, table):
        cur = self.conn.cursor()
        for field in table.fields:
            req = "ALTER TABLE "+self.ram_repr.name+".{} ADD COLUMN {} "+self.ram_repr.name+"."+field.domain
            if field.not_null:
                req += " NOT NULL"
            cur.execute(psql.SQL(req).format(psql.Identifier(table.name), psql.Identifier(field.name)))
            if field.description:
                req = "COMMENT ON COLUMN "+self.ram_repr.name+".{}.{} IS '"+table.description+"'"
                cur.execute(psql.SQL(req).format(psql.Identifier(table.name), psql.Identifier(field.name)))
        cur.close()

    def create_indices(self, table):
        cur = self.conn.cursor()
        for index in table.indices:
            req = "CREATE "
            if index.uniqueness:
                req += "UNIQUE "
            req += "INDEX {} ON "+self.ram_repr.name+".{} USING btree ("\
                   + index.field+" ASC NULLS LAST) TABLESPACE pg_default"
            cur.execute(psql.SQL(req).format(psql.Identifier(index.name), psql.Identifier(table.name)))
            if index.description:
                req = "COMMENT ON INDEX "+self.ram_repr.name+".{} IS '"+index.description+"'"
                cur.execute(psql.SQL(req).format(psql.Identifier(index.name)))
        cur.close()

    def create_constraints(self, table):
        cur = self.conn.cursor()
        for constraint in table.constraints:
            if constraint.kind == "PRIMARY":
                req = "ALTER TABLE " + self.ram_repr.name + ".{} ADD CONSTRAINT {} PRIMARY KEY ("\
                      + constraint.items + ")"
                cur.execute(psql.SQL(req).format(psql.Identifier(table.name), psql.Identifier(constraint.name)))
            if constraint.kind == "UNIQUE":
                req = "ALTER TABLE "+self.ram_repr.name+".{} ADD CONSTRAINT {} UNIQUE (" + constraint.items+")"
                cur.execute(psql.SQL(req).format(psql.Identifier(table.name), psql.Identifier(constraint.name)))
            if constraint.kind == "FOREIGN":
                req = "ALTER TABLE "+self.ram_repr.name+".{} ADD CONSTRAINT {} FOREIGN KEY (" + constraint.items+")"
                req += " REFERENCES "+self.ram_repr.name+".{} ("+constraint.items+") MATCH SIMPLE"
                req += " ON UPDATE CASCADE ON DELETE CASCADE"
                cur.execute(psql.SQL(req).format(psql.Identifier(table.name), psql.Identifier(constraint.name),
                                                 psql.Identifier(constraint.reference)))
            if constraint.description:
                req = "COMMENT ON CONSTRAINT {} ON "+self.ram_repr.name+".{} IS '"+constraint.description+"'"
                cur.execute(psql.SQL(req).format(psql.Identifier(constraint.name), psql.Identifier(table.name)))
        cur.close()
