from pixortdata import exceptions
from pixortdata import models


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
