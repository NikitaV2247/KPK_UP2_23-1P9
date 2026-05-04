from peewee import *
from datetime import date, datetime

db = SqliteDatabase('S22.db')

class BaseModel(Model):
    class Meta:
        database = db


class Group(BaseModel):
    year = IntegerField(verbose_name="Год поступления/формирования")
    active = BooleanField(default=False, verbose_name="Активна ли группа")
    student_count = IntegerField(default=0, verbose_name="Количество студентов")
    code_np = CharField(max_length=20, verbose_name="Код направления/специальности")
    number = IntegerField(verbose_name="Номер группы")
    prefix = CharField(max_length=10, verbose_name="Префикс")
    number_cl = IntegerField(verbose_name="Номер класса")

    class Meta:
        table_name = 'group'

    @property
    def full_name(self) -> str:
        """Полное имя группы (например, 1-1П9)"""
        return f"{self.year}-{self.number}{self.prefix}{self.number_cl}"


class UchPair(BaseModel):
    title = CharField(max_length=100, verbose_name="Название пары (например, '1 пара')")
    start_pair = TimeField(verbose_name="Время начала пары")
    end_pair = TimeField(verbose_name="Время окончания пары")
    duration_min = IntegerField(verbose_name="Длительность в минутах")

    class Meta:
        table_name = 'uch_pair'


class Timetable(BaseModel):
    id_pair = ForeignKeyField(UchPair, backref='timetable_entries', verbose_name="Учебная пара")
    id_group = ForeignKeyField(Group, backref='timetable_entries', verbose_name="Группа")
    day_week = IntegerField(constraints=[Check('day_week BETWEEN 1 AND 7')], verbose_name="День недели (1-7)")
    number_pair = IntegerField(verbose_name="Номер пары по порядку")
    short_day = BooleanField(default=False, verbose_name="Сокращённый день")

    class Meta:
        table_name = 'timetable'
        indexes = (
            (('id_group', 'day_week', 'number_pair'), True),
        )


def create_tables():
    db.create_tables([Group, UchPair, Timetable])

if __name__ == '__main__':
    create_tables()
