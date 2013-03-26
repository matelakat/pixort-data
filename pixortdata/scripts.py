import argparse
from pixortdata import repositories


def init():
    parser = argparse.ArgumentParser(description='Initialise a database')
    parser.add_argument('dburl', help='Database URL for SQLAlchemy')
    args = parser.parse_args()
    repositories.filesystem_alchemy_session(url=args.dburl, create_schema=True)

    from alembic.config import Config
    from alembic import command
    cfg = Config()
    cfg.set_main_option("script_location", "pixortdata:migrations")
    cfg.set_main_option("sqlalchemy.url", args.dburl)
    command.stamp(cfg, "head")
