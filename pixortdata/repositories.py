from pixortdata import exceptions
from pixortdata import models

import sqlalchemy

import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def inmemory_sa_pixort_data():
    return sa_pixort_data('sqlite:///', create_schema=True)


def sa_pixort_data(url, create_schema=False):

    def _fk_pragma_on_connect(dbapi_con, con_record):
        dbapi_con.execute('pragma foreign_keys=ON')

    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    engine = sqlalchemy.create_engine(url)

    if 'sqlite' in url:
        sqlalchemy.event.listen(engine, 'connect', _fk_pragma_on_connect)

    if create_schema:
        models.Base.metadata.create_all(engine)
    return SAPixortData(sqlalchemy.orm.sessionmaker(bind=engine)())


class Injector(object):
    def __init__(self):
        self.method = None

    def inject(self, obj):
        if self.method is not None:
            self.method(obj)
        return obj


class SARepo(object):
    def __init__(self, session, cls_to_store):
        self.session = session
        self.cls_to_store = cls_to_store
        self.injector = Injector()

    def create(self, **kwargs):
        try:
            raw = self.cls_to_store(**kwargs)
            self.session.add(raw)
            self.session.flush()
            return self.injector.inject(raw)
        except sqlalchemy.exc.IntegrityError:
            raise exceptions.DuplicateEntry(kwargs)

    def query(self, *conditions):
        q = self.session.query(self.cls_to_store)

        for condition in conditions:
            q = q.filter(condition(self.cls_to_store))

        for obj in q:
            yield self.injector.inject(obj)

    def delete(self, obj):
        self.session.delete(obj)
        self.session.flush()

    def commit(self):
        self.session.commit()


class InMemRepo(object):
    def __init__(self, cls, unique_fields):
        self._objects = []
        self._deleted_objects = []
        self.cls = cls
        self.unique_fields = unique_fields
        self.injector = Injector()

    @property
    def objects(self):
        for obj in self._objects:
            if obj in self._deleted_objects:
                continue
            yield self.injector.inject(obj)

    def create(self, **kwargs):
        new_obj = self.cls(**kwargs)

        for field in self.unique_fields:
            for obj in self.objects:
                if getattr(new_obj, field) == getattr(obj, field):
                    raise exceptions.DuplicateEntry()

        self._objects.append(new_obj)
        id = self._objects.index(new_obj)
        new_obj.id = id
        return self.injector.inject(new_obj)

    def query(self, *conditions):
        for obj in self.objects:
            if False not in [r(obj) for r in conditions]:
                yield obj

    def delete(self, obj):
        self._deleted_objects.append(obj)

    def commit(self):
        pass


class PixortData(object):
    def __init__(self, **repos):
        def inject(obj):
            for k, v in repos.items():
                setattr(obj, k, v)

        injector = Injector()
        injector.method = inject
        injector.inject(self)

        for repo in repos.values():
            repo.injector.method = inject

    def raws(self):
        return self.raw_repo.query()

    def create_raw(self, key, value):
        return self.raw_repo.create(key=key, raw_value=value)

    def keys(self):
        for obj in self.raw_repo.query():
            yield obj.key

    def raw_by_key(self, key):
        for obj in self.raw_repo.query(lambda x: x.key == key):
            return obj
        raise exceptions.NotFound(key)

    def create_classification(self, name):
        return self.classification_repo.create(name=name)

    def classifications(self):
        return self.classification_repo.query()

    def delete_classification(self, cls):
        cls.remove_all_categories()
        return self.classification_repo.delete(cls)

    def get_classification(self, name):
        for cls in self.classification_repo.query(lambda x: x.name == name):
            return cls

    def pictures(self):
        return self.picture_repo.query()

    def create_picture(self, key):
        return self.picture_repo.create(key=key)

    def get_picture(self, key):
        for pict in self.picture_repo.query(lambda x: x.key == key):
            return pict

    def commit(self):
        self.raw_repo.commit()


def SAPixortData(session):
    return PixortData(
        raw_repo=SARepo(session, models.SARaw),
        classification_repo=SARepo(session, models.SAClassification),
        tag_repo=SARepo(session, models.SATag),
        category_repo=SARepo(session, models.SACategory),
        picture_repo=SARepo(session, models.SAPicture),
    )


def InMemPixortData():
    return PixortData(
        raw_repo=InMemRepo(models.RawValue, ["key"]),
        classification_repo=InMemRepo(models.Classification, ["name"]),
        tag_repo=InMemRepo(models.Tag, []),
        category_repo=InMemRepo(models.Category, []),
        picture_repo=InMemRepo(models.Picture, ["key"]),
    )
