import unittest
from pixortdata import picture
import mock


#TODO: Add specs to Mocks
class TestAssign(unittest.TestCase):
    def test_not_assigned_thumb(self):
        assign = picture.AssignThumb()
        original = mock.Mock()
        thumb = mock.Mock()
        original.thumbnails = []

        assign(original, thumb, 100)

        original.add_thumbnail.assert_called_once_with(thumb, 100)

    def test_already_assigned_thumb(self):
        assign = picture.AssignThumb()
        original = mock.Mock()
        thumb = mock.Mock()
        original.thumbnails = [thumb]

        assign(original, thumb, "ignore")

        self.assertItemsEqual([], original.mock_calls)


class TestGetOrCreatePicture(unittest.TestCase):
    def test_get_or_create_picture_exists(self):
        pixort_data = mock.Mock()
        get_or_create = picture.GetOrCreate(pixort_data)

        pixort_data.get_picture.return_value = 'blah'

        self.assertEquals('blah', get_or_create('key1'))

        pixort_data.get_picture.assert_called_once_with('key1')

    def test_get_or_create_picture_doesnt_exists(self):
        pixort_data = mock.Mock()
        get_or_create = picture.GetOrCreate(pixort_data)

        pixort_data = get_or_create.pixort_data = mock.Mock()
        pixort_data.get_picture.return_value = None
        pixort_data.create_picture.return_value = 'blah'

        self.assertEquals('blah', get_or_create('key1'))

        pixort_data.get_picture.assert_called_once_with('key1')
        pixort_data.create_picture.assert_called_once_with('key1')
