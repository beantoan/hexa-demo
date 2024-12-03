from sqlalchemy import Table, MetaData, Column, Integer, String, Float, DateTime
from datetime import datetime

metadata = MetaData()

products = Table(
    'products',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100)),
    Column('price', Float),
    Column('description', String(500)),
    Column('created_at', DateTime, default=datetime.utcnow),
    Column('updated_at', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
)