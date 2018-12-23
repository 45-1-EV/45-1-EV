class PostDDL:

    def __init__(self, ram, usr):
        self.ram_repr = ram
        self.usr = usr
        self.DDL = ""

    def filling_db(self):
        self.DDL += "-- SCHEMA;\n"
        self.create_schema()
        self.DDL += ";\n\n-- DOMAINS"
        self.create_domains()
        self.DDL += ";\n\n-- TABLES"
        self.create_tables()
        self.DDL += ";\n\n-- FIELDS"
        for table in self.ram_repr.tables:
            self.create_fields(table)
        self.DDL += ";\n\n-- INDICES"
        for table in self.ram_repr.tables:
            self.create_indices(table)
        self.DDL += ";\n\n-- CONSTRAINTS"
        for table in self.ram_repr.tables:
            self.create_constraints(table)
        self.DDL += ";\n\n-- CONSTRAINTS (FOREIGN)"
        for table in self.ram_repr.tables:
            self.create_constraints_foreign(table)
        self.DDL += ";"
        return self.DDL

    @staticmethod
    def check_type(t):
        t = t.lower()
        if t == "blob":
            return "bytea"
        if t == "string":
            return "character varying"
        if t == "largeint":
            return "bigint"
        if t == "word":
            return "smallint"
        if t == "memo":
            return "character varying"
        if t == "byte":
            return "char"
        if t == "code":
            return "numeric"
        return t

    def create_schema(self):
        req = 'CREATE SCHEMA "'+self.ram_repr.name+'" AUTHORIZATION '+self.usr
        self.DDL += req
        if self.ram_repr.description:
            req = 'COMMENT ON SCHEMA "'+self.ram_repr.name+'" IS '+"'"+self.ram_repr.description+"'"
            self.DDL += ";\n" + req

    def create_domains(self):
        for domain in self.ram_repr.domains:
            domain.type = self.check_type(domain.type)
            req = 'CREATE DOMAIN "'+self.ram_repr.name+'"."'+domain.name+'" AS '+domain.type
            if domain.length:
                req += "("+str(domain.length)
                if domain.precision:
                    req += ","+str(domain.precision)
                req += ")"
            if domain.not_null:
                req += " NOT NULL"
            self.DDL += ";\n" + req
            if domain.description:
                req = 'COMMENT ON DOMAIN "'+self.ram_repr.name+'"."'+domain.name+'" IS '+"'"+domain.description+"'"
                self.DDL += ";\n" + req

    def create_tables(self):
        for table in self.ram_repr.tables:
            req = 'CREATE TABLE "'+self.ram_repr.name+'"."'+table.name+'" () WITH (OIDS = FALSE)'
            self.DDL += ";\n\n" + req
            req = 'ALTER TABLE "'+self.ram_repr.name+'"."'+table.name+'" OWNER to '+self.usr
            self.DDL += ";\n" + req
            if table.description:
                req = 'COMMENT ON TABLE "'+self.ram_repr.name+'"."'+table.name+'" IS '+"'"+table.description+"'"
                self.DDL += ";\n" + req

    def create_fields(self, table):
        for field in table.fields:
            req = 'ALTER TABLE "'+self.ram_repr.name+'"."'+table.name+'" ADD COLUMN "'\
                  + field.name
            if field.domain is not None:
                req += '" "'+self.ram_repr.name+'"."'+field.domain+'"'
            else:
                req += " "+field.type
            if field.not_null:
                req += " NOT NULL"
            self.DDL += ";\n\n" + req
            if field.description:
                req = 'COMMENT ON COLUMN "'+self.ram_repr.name+'"."'+table.name+'"."'\
                      + field.name+'" IS '+"'"+field.description+"'"
                self.DDL += ";\n" + req

    def create_indices(self, table):
        i = 1
        for index in table.indices:
            if index.name is None:
                index.name = table.name+"_index"+str(i)
            req = "CREATE "
            if index.uniqueness:
                req += "UNIQUE "
            req += 'INDEX "'+index.name+'" ON "'+self.ram_repr.name+'"."'+table.name+'" USING btree ("'\
                   + index.field+'" ASC NULLS LAST) TABLESPACE pg_default'
            self.DDL += ";\n\n" + req
            if index.description:
                req = 'COMMENT ON INDEX "'+self.ram_repr.name+'"."'+index.name+'" IS '+"'"+index.description+"'"
                self.DDL += ";\n" + req
            i += 1

    def create_constraints(self, table):
        i = 1
        for constraint in table.constraints:
            if constraint.kind != "FOREIGN":
                if constraint.name is None:
                    constraint.name = table.name+"_constraint"+str(i)
                if constraint.kind == "PRIMARY":
                    req = 'ALTER TABLE "' + self.ram_repr.name + '"."'+table.name+'" ADD CONSTRAINT "'\
                          + constraint.name+'" PRIMARY KEY ("' + constraint.items + '")'
                    self.DDL += ";\n\n" + req
                if constraint.kind == "UNIQUE":
                    req = 'ALTER TABLE "'+self.ram_repr.name+'"."'+table.name+'" ADD CONSTRAINT "'\
                          + constraint.name+'" UNIQUE ("' + constraint.items+'")'
                    self.DDL += ";\n\n" + req
                if constraint.description:
                    req = 'COMMENT ON CONSTRAINT "'+constraint.name+'" ON "'+self.ram_repr.name\
                          + '"."'+table.name+'" IS '+"'"+constraint.description+"'"
                    self.DDL += ";\n" + req
            i += 1

    def create_constraints_foreign(self, table):
        i = 1
        for constraint in table.constraints:
            if constraint.kind == "FOREIGN":
                if constraint.name is None:
                    constraint.name = table.name+"_constraint_f"+str(i)
                    req = 'ALTER TABLE "'+self.ram_repr.name+'"."'+table.name+'" ADD CONSTRAINT "'\
                          + constraint.name+'" FOREIGN KEY("' + constraint.items+'")'
                    req += ' REFERENCES "'+self.ram_repr.name+'"."'\
                           + constraint.reference + '" ("'+constraint.ref_field+'") MATCH SIMPLE'
                    req += " ON UPDATE CASCADE ON DELETE CASCADE"
                    self.DDL += ";\n\n" + req
                if constraint.description:
                    req = 'COMMENT ON CONSTRAINT "'+constraint.name+'" ON "'+self.ram_repr.name\
                          + '"."'+table.name+'" IS '+"'"+constraint.description+"'"
                    self.DDL += ";\n" + req
            i += 1
