from pixortdata import exceptions
from pixortdata import models

import sqlalchemy

import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def inmemory_sa_pixort_data():
    return sa_pixort_data('sqlite:///', create_schema=True)


def sa_pixort_data(url, create_schema=False):
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    engine = sqlalchemy.create_engine(url)
    if create_schema:
        models.Base.metadata.create_all(engine)
    return SAPixortData(sqlalchemy.orm.sessionmaker(bind=engine)())


class SARepo(object):
    def __init__(self, session, cls_to_store):
        self.session = session
        self.cls_to_store = cls_to_store

    def create(self, **kwargs):
        try:
            raw = self.cls_to_store(**kwargs)
            self.session.add(raw)
            self.session.flush()
            self.session.commit()
            return raw.id
        except sqlalchemy.exc.IntegrityError:
            raise exceptions.DuplicateEntry(kwargs)

    def get(self, id):
        for obj in self.query(lambda x: x.id==id):
            return obj
        raise exceptions.NotFound(id)

    def query(self, *conditions):
        q = self.session.query(self.cls_to_store)

        for condition in conditions:
            q = q.filter(condition(self.cls_to_store))

        for obj in q:
            yield obj


class InMemRepo(object):
    def __init__(self, cls, unique_fields):
        self.objects = []
        self.cls = cls
        self.unique_fields = unique_fields

    def create(self, key, raw_value):
        new_obj = self.cls(key, raw_value)

        for field in self.unique_fields:
            for obj in self.objects:
                if getattr(new_obj, field) == getattr(obj, field):
                    raise exceptions.DuplicateEntry()

        self.objects.append(new_obj)
        id = self.objects.index(new_obj)
        new_obj.id = id
        return id

    def get(self, id):
        try:
            return self.objects[id]
        except IndexError:
            raise exceptions.NotFound(id)

    def query(self, *conditions):
        for obj in self.objects:
            if False not in [r(obj) for r in conditions]:
                yield obj


class PixortData(object):
    def __init__(self, raw_repo):
        self.raw_repo = raw_repo

    def create_raw(self, key, value):
        return self.raw_repo.create(key=key, raw_value=value)

    def get_raw(self, id):
        return self.raw_repo.get(id)

    def keys(self):
        for obj in self.raw_repo.query():
            yield obj.key

    def by_key(self, key):
        for obj in self.raw_repo.query(lambda x: x.key==key):
            return obj
        raise exceptions.NotFound(key)


def SAPixortData(session):
    return PixortData(SARepo(session, models.SARaw))


def InMemPixortData():
    return PixortData(InMemRepo(models.RawValue, ["key"]))
