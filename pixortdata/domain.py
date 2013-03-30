import datetime


def suppress_exceptions(return_value=None):
    def suppress_decorator(f):
        def new_f(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except:
                if callable(return_value):
                    return return_value()
                return return_value

        return new_f

    return suppress_decorator


class Raw(object):
    def __init__(self, raw_value=None, key=None):
        self.id = None
        self.raw_value = raw_value
        self.key = key

    def categorise(self, category):
        for tag in self.tags:
            if tag.category.classification == category.classification:
                self.tag_repo.delete(tag)

        self.tag_repo.create(raw_id=self.id, category_id=category.id)

    @property
    def tags(self):
        return self.tag_repo.query(lambda x: x.raw_id == self.id)

    def get_categories(self):
        return (tag.category for tag in self.tags)

    @property
    @suppress_exceptions()
    def exif_data(self):
        for src in self.sources:
            return self.evaled['thumbnail'][src]['exif']

    @property
    def evaled(self):
        return eval(self.raw_value)

    @property
    @suppress_exceptions(lambda: [])
    def sources(self):
        result = []
        for key in self.evaled['thumbnail'].keys():
            if key not in ['format', 'size']:
                result.append(key)

        return result


class Classification(object):
    def add_category(self, name):
        return self.category_repo.create(name=name, classification_id=self.id)

    @property
    def categories(self):
        return self.category_repo.query(
            lambda x: x.classification_id == self.id)

    def remove_all_categories(self):
        for category in self.categories:
            category.delete_all_tags()
            self.category_repo.delete(category)


class Tag(object):
    @property
    def category(self):
        for cat in (
            self.category_repo.query(lambda x: x.id == self.category_id)
        ):
            return cat


class Category(object):
    @property
    def classification(self):
        for cls in (
            self.classification_repo.query(
                lambda x: x.id == self.classification_id)
        ):
            return cls

    @property
    def tags(self):
        return self.tag_repo.query(lambda x: x.category_id == self.id)

    def delete_all_tags(self):
        for tag in self.tags:
            self.tag_repo.delete(tag)


class Picture(object):
    def __init__(self, key=None):
        self.key = key

    def set_exif_info(self, exif_info):
        self.datetime = exif_info.datetime_original
        self.camera_model = exif_info.model


def _parse_exif_date(date):
    if date == "0000:00:00 00:00:00":
        return None

    return (
        date
        and datetime.datetime.strptime(
            date.strip(), "%Y:%m:%d %H:%M:%S")
    )


def parse_exif_info(raw_exif):
    date = raw_exif.get('exif:DateTimeOriginal')
    model = raw_exif.get('exif:Model')
    return ExifInfo(
        datetime_original=_parse_exif_date(date),
        model=model and model.strip())


class ExifInfo(object):
    def __init__(self, datetime_original, model):
        self.datetime_original = datetime_original
        self.model = model
