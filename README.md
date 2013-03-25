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
