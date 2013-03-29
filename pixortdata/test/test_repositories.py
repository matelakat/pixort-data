import unittest
from pixortdata import repositories
from pixortdata import exceptions
import tempfile
import os
import contextlib


class RepoTests(object):
    def test_empty(self):
        repo = self.create_repository()

        self.assertEquals([], list(repo.keys()))

    def test_id_stored_on_object(self):
        repo = self.create_repository()

        id = repo.create_raw("somekey", "somevalue")
        value = repo.get_raw(id)

        self.assertEquals(id, value.id)

    def test_create_returns_an_id(self):
        repo = self.create_repository()

        id = repo.create_raw("somekey", "somevalue")

        self.assertTrue(id is not None)

    def test_store_big_data(self):
        repo = self.create_repository()

        id = repo.create_raw("somekey", " " * 1024 * 8)
        value = repo.get_raw(id)

        self.assertEquals(" " * 1024 * 8, value.raw_value)

    def test_get_by_id(self):
        repo = self.create_repository()

        id = repo.create_raw("somekey", "somevalue")
        value = repo.get_raw(id)

        self.assertEquals("somevalue", value.raw_value)

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

    def test_get_non_existing_entry(self):
        repo = self.create_repository()

        with self.assertRaises(exceptions.NotFound):
            repo.get_raw(123)

    def test_idx_non_existing_entry(self):
        repo = self.create_repository()

        with self.assertRaises(exceptions.NotFound):
            repo.raw_by_key("stg")


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
            id = repo.create_raw('key', 'value')

            repo = self.create_repository(dburl)
            self.assertTrue(repo.get_raw(id))


class TestSAPixort(RepoTests, unittest.TestCase):
    def create_repository(self):
        return repositories.inmemory_sa_pixort_data()


class TestInMemPixort(RepoTests, unittest.TestCase):
    def create_repository(self):
        return repositories.InMemPixortData()
