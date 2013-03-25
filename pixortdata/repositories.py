from pixortdata import exceptions


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
        self.contents[id] = value
        return id

    def get(self, id):
        return self.contents[id]

    def by_key(self, key):
        id = self._keys.index(key)
        return self.contents[id]
