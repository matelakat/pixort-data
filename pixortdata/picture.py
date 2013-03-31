#TODO: Segregate the interface of pixort data
class GetOrCreate(object):
    def __init__(self, pixort_data):
        self.pixort_data = pixort_data

    def __call__(self, key):
        return (
            self.pixort_data.get_picture(key)
            or self.pixort_data.create_picture(key)
        )


class AssignThumb(object):
    def __call__(self, original, thumbnail, size):
        if thumbnail not in original.thumbnails:
            original.add_thumbnail(thumbnail, size)
