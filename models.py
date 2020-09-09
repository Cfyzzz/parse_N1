from datetime import datetime
import peewee


database = peewee.SqliteDatabase("realty.sqlite3")


class BaseTable(peewee.Model):
    # В подклассе Meta указываем подключение к той или иной базе данных
    class Meta:
        database = database


class Apartments(BaseTable):
    city = peewee.CharField(verbose_name="Город")
    district = peewee.CharField(verbose_name="Район")
    addr = peewee.CharField(verbose_name="Адрес")
    area = peewee.FloatField(verbose_name="Площадь")
    floor = peewee.IntegerField(verbose_name="Этаж")
    number_of_floors = peewee.IntegerField(default=1, verbose_name="Этажей в доме")
    material = peewee.CharField(verbose_name="Матирал")
    price = peewee.FloatField(verbose_name="Цена объекта")
    sqm = peewee.FloatField(verbose_name="Цена кв. метра")
    date = peewee.DateField(default=datetime.today(), verbose_name="Дата")


database.connect()
database.create_tables([Apartments])

