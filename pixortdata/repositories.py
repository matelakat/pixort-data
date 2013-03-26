from pixortdata import exceptions
from pixortdata import models

import sqlalchemy


class AlchemyRepo(object):
    def __init__(self):
        engine = sqlalchemy.create_engine('sqlite:///:memory:')
        models.Base.metadata.create_all(engine)
        self._session = sqlalchemy.orm.sessionmaker(bind=engine)

    def create(self, key, value):
        try:
            session = self._session()
            raw = models.SARaw(key=key, raw_value=value)
            session.add(raw)
            session.flush()
            return raw.id
        except sqlalchemy.exc.IntegrityError:
            raise exceptions.DuplicateEntry(key)

    def keys(self):
        session = self._session()
        for key, in session.query(models.SARaw.key):
            yield key

    def get(self, id):
        try:
            session = self._session()
            q = session.query(models.SARaw).filter(models.SARaw.id==id)
            return q.one()
        except sqlalchemy.orm.exc.NoResultFound:
            raise exceptions.NotFound(id)

    def by_key(self, key):
        try:
            session = self._session()
            q = session.query(models.SARaw).filter(models.SARaw.key==key)
            return q.one()
        except sqlalchemy.orm.exc.NoResultFound:
            raise exceptions.NotFound(key)


class InMemory(object):

    def __init__(self):
        self._keys = []
        self.contents = dict()

    def keys(self):
        return self._keys

    def create(self, key, value):
        if key in self._keys:
            raise exceptions.DuplicateEntry(key)
        self._keys.append(key)
        id = self._keys.index(key)
        self.contents[id] = models.RawValue(value)
        return id

    def get(self, id):
        try:
            return self.contents[id]
        except KeyError:
            raise exceptions.NotFound(id)

    def by_key(self, key):
        if key not in self._keys:
            raise exceptions.NotFound(key)

        id = self._keys.index(key)
        return self.contents[id]
