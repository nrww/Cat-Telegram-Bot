from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric, Boolean, LargeBinary
from datetime import datetime
from sqlalchemy.orm import sessionmaker, registry
import pymysql.cursors
import os

DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_LOGIN = os.environ["DB_LOGIN"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_DATABASE = os.environ["DB_DATABASE"]


conn = pymysql.connect(host=DB_HOST,
                       port=int(DB_PORT),
                       user=DB_LOGIN,
                       password=DB_PASSWORD)

with conn:
    with conn.cursor() as cursor:
        sql = f"CREATE DATABASE IF NOT EXISTS {DB_DATABASE} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        cursor.execute(sql)

    conn.commit()

engine = create_engine(f"mysql+pymysql://{DB_LOGIN}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}?charset=utf8mb4")
Session = sessionmaker(bind=engine)
metadata = MetaData()
mapper_registry = registry()

owner = Table('owner', metadata,
    Column('id', Integer(), primary_key=True),
    Column('chat_id', String(100), nullable=False),
    Column('reg_date', DateTime(), default=datetime.now),
)


cat = Table('cat', metadata,
    Column('id', Integer(), primary_key=True),
    Column('name', String(4000), nullable=False),
    Column('owner_id', ForeignKey('owner.id')),
    Column('is_pet', Boolean(), nullable=False),
)


cat_data = Table('cat_data', metadata,
    Column('id', Integer(), primary_key=True),
    Column('vector', LargeBinary(4000), nullable=False),
    Column('cat_id', ForeignKey('cat.id')),
    Column('img', String(4000)),
)


device = Table('device', metadata,
    Column('id', Integer(), primary_key=True),
    Column('name', String(200), nullable=False),
    Column('create_date', DateTime(), default=datetime.now),
    Column('owner_id', ForeignKey('owner.id')),
)


cat_log = Table('cat_log', metadata,
    Column('id', Integer(), primary_key=True),
    Column('date', DateTime(), default=datetime.now),
    Column('cat_id', ForeignKey('cat.id')),
    Column('device_id', ForeignKey('device.id')),
    Column('vector', String(4000), nullable=False),
    Column('is_openned', Boolean(), nullable=False),
    Column('has_entered', Boolean(), nullable=False),
    Column('conf', Numeric(10, 9), nullable=False)
)

metadata.create_all(engine)

class Owner(object):
    pass
class Cat(object):
    pass
class CatData(object):
    pass
class Device(object):
    pass
class CatLog(object):
    pass

mapper_registry.map_imperatively(Owner, owner)
mapper_registry.map_imperatively(Cat, cat)
mapper_registry.map_imperatively(CatData, cat_data)
mapper_registry.map_imperatively(Device, device)
mapper_registry.map_imperatively(CatLog, cat_log)