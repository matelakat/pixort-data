from pixortdata import domain


class Tag(domain.TagBO):
    def __init__(self, category_id, raw_id):
        self.category_id = category_id
        self.raw_id = raw_id


class Category(domain.CategoryBO):
    def __init__(self, name, classification_id):
        self.id = None
        self.classification_id = classification_id
        self.name = name


class Classification(domain.Classification):
    def __init__(self, name=None):
        self.id = None
        self.name = name


class RawValue(domain.Raw):
    def __init__(self, **kwargs):
        self.id = None
        self.raw_value = kwargs.get('raw_value')
        self.key = kwargs.get('key')


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class SARaw(Base, domain.Raw):
    __tablename__ = 'raw'

    id = Column(Integer, primary_key=True)
    raw_value = Column(String)
    key = Column(String, unique=True)



class SATag(Base, domain.TagBO):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    raw_id = Column(Integer, ForeignKey('raw.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))


class SACategory(Base, domain.CategoryBO):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    classification_id = Column(Integer, ForeignKey('classifications.id'))
    name = Column(String, nullable=False)


class SAClassification(Base, domain.Classification):
    __tablename__ = 'classifications'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

