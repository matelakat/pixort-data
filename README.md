# pixort-data

Data component of Pixort

## Development

Things, that are important for the development.

### Package management

All the packages are cached under `dependencies/`. Download a package by:
    
    tools/pip-download-package <package-name>

Setup your production environment by running:

    tools/pip-install-dependencies

To also set-up the test requirements, run:

    tools/pip-install-dependencies test

### Database Initialisation
To create the tables in the database, execute:

    pixort-data-init sqlite:///db

### Database Setup
Some comments to flush to a blogpost.

Initial alembic install was:

    alembic init pixortdata/migrations -t generic

After that, the file `pixortdata/migrations/env.py` had to be modified, namely
the logging configuration was removed.
