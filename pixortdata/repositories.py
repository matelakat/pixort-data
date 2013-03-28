from pixortdata import exceptions
from pixortdata import models

import sqlalchemy

import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def inmemory_alchemy_session():
    return filesystem_alchemy_session('sqlite:///', create_schema=True)


def filesystem_alchemy_session(url, create_schema=False):
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    engine = sqlalchemy.create_engine(url)
    if create_schema:
        models.Base.metadata.create_all(engine)
    return AlchemySession(sqlalchemy.orm.sessionmaker(bind=engine)())


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
        try:
            q = self.query().filter(
                self.cls_to_store.id==id)
            return q.one()
        except sqlalchemy.orm.exc.NoResultFound:
            raise exceptions.NotFound(id)

    def query(self):
        return self.session.query(self.cls_to_store)


class AlchemySession(object):
    def __init__(self, session):
        self.sarepo = SARepo(session, models.SARaw)

    def create(self, key, value):
        return self.sarepo.create(key=key, raw_value=value)

    def get(self, id):
        return self.sarepo.get(id)

    def keys(self):
        for saraw in self.sarepo.query():
            yield saraw.key

    def by_key(self, key):
        try:
            q = self.sarepo.query().filter(models.SARaw.key==key)
            return q.one()
        except sqlalchemy.orm.exc.NoResultFound:
            raise exceptions.NotFound(key)


class InMemRepo(object):
    def __init__(self, cls, unique_fields):
        self.objects = []
        self.cls = cls

    def create(self, key, raw_value):
        for obj in self.objects:
            if key == obj.key:
                raise exceptions.DuplicateEntry(key)

        obj = self.cls(key, raw_value)
        self.objects.append(obj)
        id = self.objects.index(obj)
        return id

    def get(self, id):
        try:
            return self.objects[id]
        except IndexError:
            raise exceptions.NotFound(id)


class InMemory(object):
    def __init__(self):
        self.repo = InMemRepo(models.RawValue, ["key"])

    def keys(self):
        for obj in self.repo.objects:
            yield obj.key

    def create(self, key, value):
        return self.repo.create(key=key, raw_value=value)

    def get(self, id):
        return self.repo.get(id)

    def by_key(self, key):
        for obj in self.repo.objects:
            if obj.key == key:
                return obj
        raise exceptions.NotFound(key)
