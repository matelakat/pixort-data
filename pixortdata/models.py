from pixortdata import domain


class Tag(domain.Tag):
    def __init__(self, category_id, raw_id):
        self.category_id = category_id
        self.raw_id = raw_id


class Category(domain.Category):
    def __init__(self, name, classification_id):
        self.id = None
        self.classification_id = classification_id
        self.name = name


class Classification(domain.Classification):
    def __init__(self, name=None):
        self.id = None
        self.name = name


class RawValue(domain.Raw):
    pass


class Picture(domain.Picture):
    def __init__(self, key=None, camera_model=None, datetime=None):
        self.key = key
        self.datetime = datetime
        self.camera_model = camera_model


class Relation(domain.Relation):
    pass


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship

Base = declarative_base()


class SARaw(Base, domain.Raw):
    __tablename__ = 'raw'

    id = Column(Integer, primary_key=True)
    raw_value = Column(String)
    key = Column(String, unique=True)


class SATag(Base, domain.Tag):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    raw_id = Column(Integer, ForeignKey('raw.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))


class SACategory(Base, domain.Category):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    classification_id = Column(Integer, ForeignKey('classifications.id'))
    name = Column(String, nullable=False)


class SAClassification(Base, domain.Classification):
    __tablename__ = 'classifications'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class SAPicture(Base, domain.Picture):
    __tablename__ = 'pictures'

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, nullable=False)
    camera_model = Column(String)
    datetime = Column(DateTime)

    def add_thumbnail(self, picture, size):
        self.relations_repo.create(
            src_id=picture.id,
            relation_name="thumb_of",
            tgt_id=self.id,
            size=size)


class SARelation(Base, domain.Relation):
    __tablename__ = 'relations'
    __table_args__ = (
        UniqueConstraint(
            'relation_name', 'src_id', 'tgt_id'),
    )

    id = Column(Integer, primary_key=True)
    relation_name = Column(String, nullable=False)
    size = Column(Integer)

    src_id = Column(Integer, ForeignKey('pictures.id'), nullable=False)
    tgt_id = Column(Integer, ForeignKey('pictures.id'), nullable=False)
