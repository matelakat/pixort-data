class RawValue(object):
    def __init__(self, key, raw_value):
        self.raw_value = raw_value
        self.key = key


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class SARaw(Base):
    __tablename__ = 'raw'

    id = Column(Integer, primary_key=True)
    raw_value = Column(String)
    key = Column(String, unique=True)


class SAClassification(Base):
    __tablename__ = 'classifications'

    id = Column(Integer, primary_key=True)
    category = Column(String)
    key = Column(String, unique=True)
