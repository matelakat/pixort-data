import argparse
from pixortdata import repositories
from pixortdata import domain
from pixortdata import picture


def categories(argv=None):
    parser = argparse.ArgumentParser(description='Load categories from a file')
    parser.add_argument('dburl', help='Database URL for SQLAlchemy')
    parser.add_argument('classification', help='Name of classification')
    parser.add_argument('default_category',
                        help='Default tag for non classified ones')
    parser.add_argument('fname', help='Name of the file to load')
    args = parser.parse_args(args=argv)

    repo = repositories.sa_pixort_data(url=args.dburl)

    cls = repo.get_classification(args.classification)
    if cls:
        repo.delete_classification(cls)

    cls = repo.create_classification(args.classification)

    def _get_category(name):
        for category in cls.categories:
            if category.name == name:
                return category

        return cls.add_category(name)

    with open(args.fname, 'rb') as tags:
        for line in tags:
            category_name = args.default_category
            splitted = line.split()
            if len(splitted) > 1:
                category_name = splitted[1]

            key = splitted[0]

            raw = repo.raw_by_key(key)

            category = _get_category(category_name)
            raw.categorise(category)

    repo.commit()


def exif(argv=None):
    parser = argparse.ArgumentParser(
        description='Create exif info from raw data')
    parser.add_argument('dburl', help='Database URL for SQLAlchemy')
    args = parser.parse_args(args=argv)

    repo = repositories.sa_pixort_data(url=args.dburl)

    for raw in repo.raws():
        if raw.exif_data:
            exif_info = domain.parse_exif_info(raw.exif_data)

            for key in raw.sources:
                pict = repo.get_picture(key) or repo.create_picture(key)
                pict.set_exif_info(exif_info)

    repo.commit()


def thumbs(argv=None):
    parser = argparse.ArgumentParser(
        description='Create exif info from raw data')
    parser.add_argument('dburl', help='Database URL for SQLAlchemy')
    args = parser.parse_args(args=argv)

    pixort_data = repositories.sa_pixort_data(url=args.dburl)
    picture_get_or_create = picture.GetOrCreate(pixort_data)
    assign_thumb = picture.AssignThumb()

    for raw in pixort_data.raws():
        if raw.is_thumb:
            thumbnail = picture_get_or_create(raw.key)

            for source_key in raw.sources:
                original = picture_get_or_create(source_key)

                assign_thumb(
                    original=original, thumbnail=thumbnail, size=raw.size)

    pixort_data.commit()
