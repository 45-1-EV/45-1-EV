from modules.post_ddl import PostDDL
from db import db_classes as dbc


ram = dbc.Schema()
ram.name = "edo"
ram.description = "des"
d = dbc.Domain()
d.name = "dom"
d.type = "numeric"
d.length = 10
d.precision = 5
d.description = "test dom"
t = dbc.Table()
t.name = "test_table"
t.description = "desc"
f = dbc.Field()
f.name = "field"
f.description = "field desc"
f.domain = "dom"
i = dbc.Index()
i.uniqueness = True
i.description = "i desc"
i.name = "index1"
i.field = f.name
c = dbc.Constraint()
c.name = "constraint1"
c.description = "c desc"
c.kind = "PRIMARY"
c.items = f.name
t.fields.append(f)
t.indices.append(i)
t.constraints.append(c)
ram.domains.append(d)
ram.tables.append(t)
PostDDL(ram, "Test", "postgres", "123").filling_db()
