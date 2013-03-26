from setuptools import setup


setup(
    name="pixortdata",
    version="0.0",
    packages=["pixortdata"],
    entry_points={
        'console_scripts': [
            'pixort-data-init = pixortdata.scripts:init',
        ]
    }
)
