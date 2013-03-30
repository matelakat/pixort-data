import argparse
from pixortdata import repositories


def categories(args=None):
    parser = argparse.ArgumentParser(description='Load categories from a file')
    parser.add_argument('dburl', help='Database URL for SQLAlchemy')
    parser.add_argument('classification', help='Name of classification')
    parser.add_argument('default_category',
                        help='Default tag for non classified ones')
    parser.add_argument('fname', help='Name of the file to load')
    args = parser.parse_args(args=args or sys.argv)

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
