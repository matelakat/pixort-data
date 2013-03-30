class RawBO(object):
    def categorise(self, category):
        for tag in self.tags:
            if tag.category.classification == category.classification:
                self.tag_repo.delete(tag.id)

        self.tag_repo.create(raw_id=self.id, category_id=category.id)

    @property
    def tags(self):
        return self.tag_repo.query(lambda x: x.raw_id==self.id)

    def get_categories(self):
        return (tag.category for tag in self.tags)


class ClassificationBO(object):
    def add_category(self, name):
        return self.category_repo.create(name=name, classification_id=self.id)

    @property
    def categories(self):
        return self.category_repo.query(lambda x: x.classification_id==self.id)

    def remove_all_categories(self):
        for category in self.categories:
            category.delete_all_tags()
            self.category_repo.delete(category.id)


class TagBO(object):
    @property
    def category(self):
        for cat in self.category_repo.query(lambda x: x.id==self.category_id):
            return cat


class CategoryBO(object):
    @property
    def classification(self):
        for cls in self.classification_repo.query(lambda x: x.id==self.classification_id):
            return cls

    @property
    def tags(self):
        return self.tag_repo.query(lambda x: x.category_id==self.id)

    def delete_all_tags(self):
        for tag in self.tags:
            self.tag_repo.delete(tag.id)


class Tag(TagBO):
    def __init__(self, category_id, raw_id):
        self.category_id = category_id
        self.raw_id = raw_id


class Category(CategoryBO):
    def __init__(self, name, classification_id):
        self.id = None
        self.classification_id = classification_id
        self.name = name


class Classification(ClassificationBO):
    def __init__(self, name=None):
        self.id = None
        self.name = name


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



class SATag(Base, TagBO):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    raw_id = Column(Integer, ForeignKey('raw.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))


class SACategory(Base, CategoryBO):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    classification_id = Column(Integer, ForeignKey('classifications.id'))
    name = Column(String, nullable=False)


class SAClassification(Base, ClassificationBO):
    __tablename__ = 'classifications'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

