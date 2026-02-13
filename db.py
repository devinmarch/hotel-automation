from peewee import SqliteDatabase, Model, CharField

db = SqliteDatabase('ha.db')

class BaseModel(Model):
    class Meta:
        database = db

class Reservations(BaseModel):
    reservation_id = CharField(primary_key=True)
    date_modified = CharField()
    status = CharField()
    guest_name = CharField()
    start_date = CharField()
    end_date = CharField()
    balance = CharField()

db.connect()
db.create_tables([Reservations])