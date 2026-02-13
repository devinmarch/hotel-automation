from peewee import SqliteDatabase, Model, CharField, ForeignKeyField, CompositeKey

db = SqliteDatabase('ha.db')

db.pragma('foreign_keys', 1, permanent=True)

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

class Assignments(BaseModel):
    reservation = ForeignKeyField(Reservations, backref='assignments', on_delete='CASCADE')
    room_id = CharField()
    room_status = CharField()
    room_check_in = CharField()
    room_check_out = CharField()

    class Meta:
        primary_key = CompositeKey('reservation', 'room_id')

db.connect(reuse_if_open=True)
db.create_tables([Reservations, Assignments])