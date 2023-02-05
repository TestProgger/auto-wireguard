from peewee import SqliteDatabase , Model
from peewee import AutoField , TextField , IntegerField , DateTimeField
from datetime import datetime

db = SqliteDatabase('db.sqlite3')

class Client(Model):
    id = AutoField(primary_key=True)
    name = TextField(null=False)
    client_id = IntegerField( null=False)
    host_id = IntegerField( null=False)

    private_key = TextField(null=False)
    public_key = TextField(null=False)
    pre_shared_key = TextField(null=False)

    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db

