import unittest
from pixortdata import repositories
from pixortdata import exceptions
import tempfile
import os
import contextlib


class RawTests(object):
    def test_empty(self):
        repo = self.create_repository()

        self.assertEquals([], list(repo.keys()))

    def test_id_stored_on_object(self):
        repo = self.create_repository()

        raw = repo.create_raw("somekey", "somevalue")

        self.assertFalse(raw is None)

    def test_store_big_data(self):
        repo = self.create_repository()

        raw = repo.create_raw("somekey", " " * 1024 * 8)

        self.assertEquals(" " * 1024 * 8, raw.raw_value)

    def test_get_by_key(self):
        repo = self.create_repository()

        repo.create_raw("somekey", "somevalue")
        value = repo.raw_by_key("somekey")

        self.assertEquals("somevalue", value.raw_value)

    def test_non_empty_listing(self):
        repo = self.create_repository()

        repo.create_raw("somekey", "somevalue")

        self.assertEquals(["somekey"], [k for k in repo.keys()])

    def test_duplicate_entry(self):
        repo = self.create_repository()

        repo.create_raw("somekey", "somevalue")

        with self.assertRaises(exceptions.DuplicateEntry):
            repo.create_raw("somekey", "othervalue")

    def test_idx_non_existing_entry(self):
        repo = self.create_repository()

        with self.assertRaises(exceptions.NotFound):
            repo.raw_by_key("stg")


class TagTests(object):
    def test_create(self):
        repo = self.create_repository()

        cls = repo.create_classification("classification")

        self.assertFalse(cls is None)
        self.assertEquals("classification", cls.name)

    def test_create_same_name(self):
        repo = self.create_repository()
        repo.create_classification("classification")

        with self.assertRaises(exceptions.DuplicateEntry):
            repo.create_classification("classification")

    def test_list_classifications_empty(self):
        repo = self.create_repository()

        self.assertItemsEqual([], repo.classifications())

    def test_list_classifications_non_empty(self):
        repo = self.create_repository()

        cls = repo.create_classification("classification")

        self.assertItemsEqual([cls], repo.classifications())

    def test_delete_classification(self):
        repo = self.create_repository()
        cls = repo.create_classification("classification")

        repo.delete_classification(cls.id)

        self.assertItemsEqual([], repo.classifications())

    def test_categories_are_empty(self):
        repo = self.create_repository()
        cls = repo.create_classification("classification")

        self.assertItemsEqual([], cls.categories)

    def test_add_category(self):
        repo = self.create_repository()
        cls = repo.create_classification("classification")

        cat = cls.add_category("cat1")

        self.assertItemsEqual([cat], cls.categories)

    def test_tag_existing_raw(self):
        repo = self.create_repository()
        raw = repo.create_raw('key', 'value')
        cls = repo.create_classification("classification")
        cat1 = cls.add_category("cat1")

        raw.tag_with(cat1)


class RepoTests(RawTests, TagTests):
    pass


@contextlib.contextmanager
def tempdb():
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        tf.close()
        try:
            yield "sqlite:///" + os.path.abspath(tf.name)
        finally:
            os.unlink(tf.name)


class TestPersistency(unittest.TestCase):
    def create_repository(self, url):
        return repositories.sa_pixort_data(
            url, create_schema=True)

    def test_change_persists(self):
        with tempdb() as dburl:
            repo = self.create_repository(dburl)
            repo.create_raw('key', 'value')

            repo = self.create_repository(dburl)
            self.assertEquals('value', repo.raw_by_key('key').raw_value)


class TestSAPixort(RepoTests, unittest.TestCase):
    def create_repository(self):
        return repositories.inmemory_sa_pixort_data()


class TestInMemPixort(RepoTests, unittest.TestCase):
    def create_repository(self):
        return repositories.InMemPixortData()
