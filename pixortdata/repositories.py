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
        return self.objects.index(new_obj)

    def get(self, id):
        try:
            return self.objects[id]
        except IndexError:
            raise exceptions.NotFound(id)

    def query(self, *conditions):
        for obj in self.objects:
            if False not in [r(obj) for r in conditions]:
                yield obj


class RawRepo(object):
    def __init__(self, repo):
        self.repo = repo

    def create(self, key, value):
        return self.repo.create(key=key, raw_value=value)

    def get(self, id):
        return self.repo.get(id)

    def keys(self):
        for obj in self.repo.query():
            yield obj.key

    def by_key(self, key):
        for obj in self.repo.query(lambda x: x.key==key):
            return obj
        raise exceptions.NotFound(key)


class AlchemySession(RawRepo):
    def __init__(self, session):
        super(AlchemySession, self).__init__(SARepo(session, models.SARaw))


class InMemory(RawRepo):
    def __init__(self):
        super(InMemory, self).__init__(InMemRepo(models.RawValue, ["key"]))

