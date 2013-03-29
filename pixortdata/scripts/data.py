import argparse
from pixortdata import repositories
from alembic.config import Config
from alembic import command


def _get_config(dburl):
    cfg = Config()
    cfg.set_main_option("script_location", "pixortdata:migrations")
    cfg.set_main_option("sqlalchemy.url", dburl)
    return cfg


def init():
    parser = argparse.ArgumentParser(description='Initialise a database')
    parser.add_argument('dburl', help='Database URL for SQLAlchemy')
    args = parser.parse_args()
    repositories.filesystem_alchemy_session(url=args.dburl, create_schema=True)

    command.stamp(_get_config(args.dburl), "head")


def version():
    parser = argparse.ArgumentParser(
        description='Print out the actual version of the database')
    parser.add_argument('dburl', help='Database URL for SQLAlchemy')
    args = parser.parse_args()
    repositories.filesystem_alchemy_session(url=args.dburl)

    command.current(_get_config(args.dburl))


def upgrade():
    parser = argparse.ArgumentParser(description='Upgrade database schema')
    parser.add_argument('dburl', help='Database URL for SQLAlchemy')
    args = parser.parse_args()
    repositories.filesystem_alchemy_session(url=args.dburl)

    command.upgrade(_get_config(args.dburl), "head")


def revision():
    parser = argparse.ArgumentParser(description='Create a new db revision')
    parser.add_argument('dburl', help='Database URL for SQLAlchemy')
    parser.add_argument('message', help='Message for the new version')
    parser.add_argument('--autogenerate', help='Autogenerate',
                        action='store_true')
    args = parser.parse_args()
    repositories.filesystem_alchemy_session(url=args.dburl)

    command.revision(_get_config(args.dburl), message=args.message, autogenerate=args.autogenerate)
