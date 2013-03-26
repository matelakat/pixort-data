from setuptools import setup


setup(
    name="pixortdata",
    version="0.0",
    packages=["pixortdata"],
    entry_points={
        'console_scripts': [
            'pixort-data-init = pixortdata.scripts:init',
            'pixort-data-version = pixortdata.scripts:version',
            'pixort-data-upgrade = pixortdata.scripts:upgrade',
            'pixort-data-revision = pixortdata.scripts:revision',
        ]
    }
)
