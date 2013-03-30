import unittest
from pixortdata.test import utils
from pixortdata.scripts import load
from pixortdata import repositories


class TestLoadCategories(unittest.TestCase):
    def create_repository(self, url):
        return repositories.sa_pixort_data(
            url, create_schema=True)

    def load(self, dburl, lines):
        with utils.tempfname() as fname:
            with open(fname, 'wb') as f:
                for l in lines:
                    f.write('%s\n' % l)
                f.close()

                args = [dburl, 'test import', '0', fname]

                load.categories(args)

    def test_load_default_category(self):
        with utils.tempdb() as dburl:
            repo = self.create_repository(dburl)
            repo.create_raw('key', 'value')

            self.load(dburl, ['key'])

            cls, = repo.classifications()
            self.assertItemsEqual('test import', cls.name)
            self.assertItemsEqual(['0'], [c.name for c in cls.categories])
            raw = repo.raw_by_key('key')
            self.assertItemsEqual(['0'], [c.name for c in raw.get_categories()]) 

    def test_load_multiple_lines(self):
        with utils.tempdb() as dburl:
            repo = self.create_repository(dburl)
            repo.create_raw('key', 'value')

            self.load(dburl, ['key', 'key 3', 'key'])

            cls, = repo.classifications()
            self.assertItemsEqual('test import', cls.name)
            self.assertItemsEqual(['0', '3'], [c.name for c in cls.categories])
            raw = repo.raw_by_key('key')
            self.assertItemsEqual(['0'], [c.name for c in raw.get_categories()])

    def test_load_multiple_times(self):
        with utils.tempdb() as dburl:
            repo = self.create_repository(dburl)
            repo.create_raw('key', 'value')
            repo.create_raw('key1', 'value')

            self.load(dburl, ['key', 'key 3', 'key'])
            self.load(dburl, ['key1 87', 'key 3', 'key'])

            cls, = repo.classifications()
            self.assertItemsEqual('test import', cls.name)
            self.assertItemsEqual(['0', '3', '87'], [c.name for c in cls.categories])
            raw = repo.raw_by_key('key')
            self.assertItemsEqual(['0'], [c.name for c in raw.get_categories()])

            raw = repo.raw_by_key('key1')
            self.assertItemsEqual(['87'], [c.name for c in raw.get_categories()])
