class RawBO(object):
    def tag_with(self, category):
        pass


class ClassificationBO(object):
    def add_category(self, name):
        cat = self._create_category(name)
        self.categories.append(cat)
        return cat


class Category(object):
    def __init__(self, name):
        self.name = name


class Classification(ClassificationBO):
    def __init__(self, name=None):
        self.id = None
        self.name = name
        self.categories = []

    def _create_category(self, name):
        return Category(name=name)


class RawValue(RawBO):
    def __init__(self, **kwargs):
        self.id = None
        self.raw_value = kwargs.get('raw_value')
        self.key = kwargs.get('key')


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class SARaw(Base, RawBO):
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


class SAClassification(Base, ClassificationBO):
    __tablename__ = 'classifications'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    categories = relationship("SACategory")

    def _create_category(self, name):
        return SACategory(name=name)
