from pixortdata import domain
import datetime

import unittest


class TestRawIsThumb(unittest.TestCase):
    def test_is_thumb_on_thumbnail(self):
        thumb_data = repr({'thumbnail': {}})

        raw = domain.Raw(raw_value=thumb_data)

        self.assertTrue(raw.is_thumb)

    def test_is_thumb_on_non_thumbnail(self):
        thumb_data = repr({})

        raw = domain.Raw(raw_value=thumb_data)

        self.assertFalse(raw.is_thumb)

    def test_is_thumb_on_invalid(self):
        thumb_data = 'invalid'

        raw = domain.Raw(raw_value=thumb_data)

        self.assertFalse(raw.is_thumb)


class TestRawSize(unittest.TestCase):
    def test_proper_data(self):
        thumb_data = repr({'thumbnail': {'size': 100}})

        raw = domain.Raw(raw_value=thumb_data)

        self.assertEquals(100, raw.size)

    def test_invalid_data(self):
        thumb_data = 'blah'

        raw = domain.Raw(raw_value=thumb_data)

        self.assertEquals(None, raw.size)


class TestExif(unittest.TestCase):
    def test_exif_info_on_thumb(self):
        thumb_data = repr({
            'thumbnail': {
                'size': 100,
                'key1': {
                    'exif': {
                        'exifkey': 'exifvalue'
                    }
                }
            }
        })

        raw = domain.Raw(raw_value=thumb_data)

        self.assertEquals(dict(exifkey='exifvalue'), raw.exif_data)

    def test_exif_info_non_valid_python(self):
        thumb_data = 'blah'

        raw = domain.Raw(raw_value=thumb_data)

        self.assertEquals(None, raw.exif_data)

    def test_exif_info_invalid_data(self):
        thumb_data = repr({
            'thumbnail': {
                'format': 100,
                'size': 100,
                'key1': {},
            }
        })

        raw = domain.Raw(raw_value=thumb_data)

        self.assertEquals(None, raw.exif_data)


class TestSources(unittest.TestCase):
    def test_sources(self):
        thumb_data = repr({
            'thumbnail': {
                'format': 100,
                'size': 100,
                'key1': {},
                'key2': {
                    'exif': {
                        'exifkey': 'exifvalue'
                    },
                }
            }
        })

        raw = domain.Raw(raw_value=thumb_data)

        self.assertItemsEqual(['key1', 'key2'], raw.sources)

    def test_invalid_src(self):
        thumb_data = 'ii'

        raw = domain.Raw(raw_value=thumb_data)

        self.assertItemsEqual([], raw.sources)


class TestPicture(unittest.TestCase):
    def test_create(self):
        picture = domain.Picture()
        now = datetime.datetime.now()

        picture.set_exif_info(
            domain.ExifInfo(
                datetime_original=now,
                model="model"))

        self.assertEquals(now, picture.datetime)
        self.assertEquals('model', picture.camera_model)


class TestParseExifInfo(unittest.TestCase):
    def test_create(self):
        raw_info = {
            'exif:DateTimeOriginal': '2007:08:20 11:10:38',
            'exif:Model': 'FinePix S9500  '
        }

        exif = domain.parse_exif_info(raw_info)

        self.assertEquals('FinePix S9500', exif.model)
        self.assertEquals(
            datetime.datetime(2007, 8, 20, 11, 10, 38),
            exif.datetime_original
        )

    def test_invalid_date(self):
        raw_info = {
            'exif:DateTimeOriginal': '0000:00:00 00:00:00',
        }

        exif = domain.parse_exif_info(raw_info)

        self.assertEquals(
            None,
            exif.datetime_original
        )

    def test_empty_data(self):
        raw_info = dict()

        exif = domain.parse_exif_info(raw_info)

        self.assertEquals(None, exif.model)
        self.assertEquals(
            None,
            exif.datetime_original
        )
