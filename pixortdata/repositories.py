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
            return raw
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

    def delete(self, id):
        self.session.delete(self.get(id))
        self.session.commit()


class InMemRepo(object):
    def __init__(self, cls, unique_fields):
        self._objects = []
        self._deleted_objects = []
        self.cls = cls
        self.unique_fields = unique_fields

    @property
    def objects(self):
        for obj in self._objects:
            if obj in self._deleted_objects:
                continue
            yield obj

    def create(self, **kwargs):
        new_obj = self.cls(**kwargs)

        for field in self.unique_fields:
            for obj in self.objects:
                if getattr(new_obj, field) == getattr(obj, field):
                    raise exceptions.DuplicateEntry()

        self._objects.append(new_obj)
        id = self._objects.index(new_obj)
        new_obj.id = id
        return new_obj

    def get(self, id):
        for obj in self.objects:
            if id == obj.id:
                return obj
        raise exceptions.NotFound(id)

    def query(self, *conditions):
        for obj in self.objects:
            if False not in [r(obj) for r in conditions]:
                yield obj

    def delete(self, id):
        self._deleted_objects.append(self.get(id))


class PixortData(object):
    def __init__(self, raw_repo, category_repo):
        self.raw_repo = raw_repo
        self.category_repo = category_repo

    def create_raw(self, key, value):
        return self.raw_repo.create(key=key, raw_value=value)

    def get_raw(self, id):
        return self.raw_repo.get(id)

    def keys(self):
        for obj in self.raw_repo.query():
            yield obj.key

    def raw_by_key(self, key):
        for obj in self.raw_repo.query(lambda x: x.key==key):
            return obj
        raise exceptions.NotFound(key)

    def create_classification(self, name):
        return self.category_repo.create(name=name)

    def classifications(self):
        return self.category_repo.query()

    def delete_classification(self, id):
        return self.category_repo.delete(id)



def SAPixortData(session):
    return PixortData(
        SARepo(session, models.SARaw),
        SARepo(session, models.SAClassification)
    )


def InMemPixortData():
    return PixortData(
        InMemRepo(models.RawValue, ["key"]),
        InMemRepo(models.Classification, ["name"])
    )
