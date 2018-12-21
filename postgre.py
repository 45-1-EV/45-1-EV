from modules.post_ddl import PostDDL
from db import db_classes as dbc


ram = dbc.Schema()

PostDDL(ram, "Test", "postgres", "123").filling_db()
