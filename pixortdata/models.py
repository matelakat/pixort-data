class RawValue(object):
    def __init__(self, key, raw_value):
        self.id = None
        self.raw_value = raw_value
        self.key = key


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()


class SARaw(Base):
    __tablename__ = 'raw'

    id = Column(Integer, primary_key=True)
    raw_value = Column(String)
    key = Column(String, unique=True)


class SATag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    raw_id = Column(Integer, ForeignKey('raw.id'))
    tag_id = Column(Integer, ForeignKey('tags.id'))


class SACategory(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    classification_id = Column(Integer, ForeignKey('classifications.id'))
    name = Column(String, nullable=False)


class SAClassification(Base):
    __tablename__ = 'classifications'

    id = Column(Integer, primary_key=True)
    category = Column(String)
