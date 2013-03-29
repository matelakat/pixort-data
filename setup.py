from setuptools import setup


setup(
    name="pixortdata",
    version="0.0",
    packages=["pixortdata"],
    entry_points={
        'console_scripts': [
            'pixort-data-init = pixortdata.scripts.data:init',
            'pixort-data-version = pixortdata.scripts.data:version',
            'pixort-data-upgrade = pixortdata.scripts.data:upgrade',
            'pixort-data-revision = pixortdata.scripts.data:revision',
        ]
    }
)
