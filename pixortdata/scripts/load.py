import argparse
from pixortdata import repositories


def categories():
    parser = argparse.ArgumentParser(description='Load categories from a file')
    parser.add_argument('dburl', help='Database URL for SQLAlchemy')
    parser.add_argument('classification', help='Name of classification')
    parser.add_argument('default_tag', help='Default tag for non classified ones')
    args = parser.parse_args()

    repositories.sa_pixort_data(url=args.dburl)
