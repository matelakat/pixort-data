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
