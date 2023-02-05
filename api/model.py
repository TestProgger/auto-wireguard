from peewee import SqliteDatabase , Model
from peewee import AutoField , TextField , IntegerField

class User(Model):
    id = AutoField(primary_key=True)
    client_id = IntegerField()
    host_id = IntegerField()

db = SqliteDatabase('db.sqlite3')
db.create_tables([User , ])