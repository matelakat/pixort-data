import unittest
from pixortdata import repositories
from pixortdata import exceptions
from pixortdata.test import utils
import datetime


class RawTests(object):
    def test_empty(self):
        repo = self.create_repository()

        self.assertEquals([], list(repo.keys()))

    def test_id_stored_on_object(self):
        repo = self.create_repository()

        raw = repo.create_raw("somekey", "somevalue")
        repo.commit()

        self.assertFalse(raw is None)

    def test_store_big_data(self):
        repo = self.create_repository()

        raw = repo.create_raw("somekey", " " * 1024 * 8)
        repo.commit()

        self.assertEquals(" " * 1024 * 8, raw.raw_value)

    def test_store_retrieve(self):
        repo = self.create_repository()

        raw = repo.create_raw("somekey", "v1")
        raw2 = repo.create_raw("somekey2", "v1")
        repo.commit()

        self.assertItemsEqual([raw, raw2], repo.raws())

    def test_get_by_key(self):
        repo = self.create_repository()

        repo.create_raw("somekey", "somevalue")
        repo.commit()
        value = repo.raw_by_key("somekey")

        self.assertEquals("somevalue", value.raw_value)

    def test_non_empty_listing(self):
        repo = self.create_repository()

        repo.create_raw("somekey", "somevalue")
        repo.commit()

        self.assertEquals(["somekey"], [k for k in repo.keys()])

    def test_duplicate_entry(self):
        repo = self.create_repository()

        repo.create_raw("somekey", "somevalue")
        repo.commit()

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
        repo.commit()

        self.assertFalse(cls is None)
        self.assertEquals("classification", cls.name)

    def test_create_same_name(self):
        repo = self.create_repository()
        repo.create_classification("classification")
        repo.commit()

        with self.assertRaises(exceptions.DuplicateEntry):
            repo.create_classification("classification")

    def test_list_classifications_empty(self):
        repo = self.create_repository()

        self.assertItemsEqual([], repo.classifications())

    def test_list_classifications_non_empty(self):
        repo = self.create_repository()

        cls = repo.create_classification("classification")
        repo.commit()

        self.assertItemsEqual([cls], repo.classifications())

    def test_delete_classification(self):
        repo = self.create_repository()
        cls = repo.create_classification("classification")
        repo.commit()

        repo.delete_classification(cls)
        repo.commit()

        self.assertItemsEqual([], repo.classifications())

    def test_categories_are_empty(self):
        repo = self.create_repository()
        cls = repo.create_classification("classification")
        repo.commit()

        self.assertItemsEqual([], cls.categories)

    def test_add_category(self):
        repo = self.create_repository()
        cls = repo.create_classification("classification")

        cat = cls.add_category("cat1")
        repo.commit()

        self.assertItemsEqual([cat], cls.categories)

    def test_categorise_existing_raw(self):
        repo = self.create_repository()
        raw = repo.create_raw('key', 'value')
        cls = repo.create_classification("classification")

        cat1 = cls.add_category("cat1")

        raw.categorise(cat1)
        repo.commit()

        self.assertItemsEqual([cat1], raw.get_categories())

    def test_amend_category(self):
        repo = self.create_repository()
        raw = repo.create_raw('key', 'value')
        cls = repo.create_classification("classification")

        cat1 = cls.add_category("cat1")
        cat2 = cls.add_category("cat2")

        raw.categorise(cat1)
        raw.categorise(cat2)

        self.assertItemsEqual([cat2], raw.get_categories())

    def test_delete_classification_with_tags(self):
        repo = self.create_repository()
        raw = repo.create_raw('key', 'value')
        cls = repo.create_classification("classification")
        cat1 = cls.add_category("cat1")
        raw.categorise(cat1)

        repo.delete_classification(cls)
        repo.commit()

        self.assertItemsEqual([], repo.classifications())

    def test_get_classification(self):
        repo = self.create_repository()
        cls = repo.create_classification("classification")

        cls2 = repo.get_classification('classification')

        self.assertEquals(cls, cls2)


class PictureTests(object):
    def test_pictures_is_empty(self):
        repo = self.create_repository()

        self.assertItemsEqual([], repo.pictures())

    def test_create_picture(self):
        repo = self.create_repository()

        pict = repo.create_picture('key')

        self.assertItemsEqual([pict], repo.pictures())

    def test_get_picture_after_created(self):
        repo = self.create_repository()

        pict = repo.create_picture('key')

        self.assertEquals(pict, repo.get_picture('key'))

    def test_get_non_existing_picture(self):
        repo = self.create_repository()

        self.assertEquals(None, repo.get_picture('key'))

    def test_picture_fields_stored(self):
        repo = self.create_repository()

        pict = repo.create_picture('key')
        self.assertTrue(hasattr(pict, 'camera_model'))
        self.assertTrue(hasattr(pict, 'datetime'))

        pict.camera_model = "camera"
        pict.datetime = datetime.datetime.now()

        self.assertItemsEqual([pict], repo.pictures())


class ThumbnailTests(object):
    def test_get_thumbs(self):
        repo = self.create_repository()

        pict = repo.create_picture('key')

        self.assertItemsEqual([], pict.thumbnails)

    def test_add_thumbnail(self):
        repo = self.create_repository()

        pict = repo.create_picture('key')
        thumb = repo.create_picture('key2')

        pict.add_thumbnail(thumb, 100)

        self.assertItemsEqual([thumb], pict.thumbnails)


class RepoTests(RawTests, TagTests, PictureTests, ThumbnailTests):
    pass


class TestPersistency(unittest.TestCase):
    def create_repository(self, url):
        return repositories.sa_pixort_data(
            url, create_schema=True)

    def test_change_persists(self):
        with utils.tempdb() as dburl:
            repo = self.create_repository(dburl)
            repo.create_raw('key', 'value')
            repo.commit()

            repo = self.create_repository(dburl)
            self.assertEquals('value', repo.raw_by_key('key').raw_value)


class TestSAPixort(RepoTests, unittest.TestCase):
    def create_repository(self):
        return repositories.inmemory_sa_pixort_data()


class TestInMemPixort(RepoTests, unittest.TestCase):
    def create_repository(self):
        return repositories.InMemPixortData()
