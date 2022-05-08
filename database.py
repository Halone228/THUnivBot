from peewee import *

db = SqliteDatabase('db.db')


class BaseModel(Model):
    class Meta:
        database = db


class UserModel(BaseModel):
    user_id = BigIntegerField(null=False,
                              unique=True,
                              column_name='id',
                              primary_key=True)
    last_message_id = BigIntegerField(null=True)
    subscription = BooleanField(null=True)
    people_class = SmallIntegerField(null=True)  # -1 - Поступающий, 0 - Студент, 1 - Преподователь
    queue = TextField(null=True)
    that = TextField(null=True)

    @classmethod
    def get_by_id(cls, value):
        if cls.select().where(cls.user_id == value).get_or_none() is None:
            usr = cls()
            usr.user_id = value
            usr.save(force_insert=True)
            return usr
        else:
            return cls.get(cls.user_id == value)


UserModel.create_table()
UserModel.validate_model()


def close_db():
    db.close()
