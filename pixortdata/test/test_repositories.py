import unittest
from pixortdata import repositories


class TestRawRepo(unittest.TestCase):
    def create_repository(self):
        return repositories.InMemory()

    def test_empty(self):
        repo = self.create_repository()

        self.assertEquals([], list(repo.keys()))

    def test_create_returns_an_id(self):
        repo = self.create_repository()

        id = repo.create("somekey", "somevalue")

        self.assertTrue(id is not None)

    def test_get_by_id(self):
        repo = self.create_repository()

        id = repo.create("somekey", "somevalue")
        value = repo.get(id)

        self.assertEquals("somevalue", value)

    def test_get_by_key(self):
        repo = self.create_repository()

        repo.create("somekey", "somevalue")
        value = repo.by_key("somekey")

        self.assertEquals("somevalue", value)

    def test_non_empty_listing(self):
        repo = self.create_repository()

        repo.create("somekey", "somevalue")

        self.assertEquals(["somekey"], list(repo.keys()))
