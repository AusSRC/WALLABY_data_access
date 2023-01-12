import os
import re
from setuptools import setup

# Set version as environment variable
semver_regex = re.compile(r'\d{1}.\d{1}.\d{1}')
if 'VERSION' not in os.environ:
    raise Exception('Set version as environment variable (e.g. export VERSION=1.0.0)')
version = os.getenv('VERSION')
match = semver_regex.search(version)
if match is None:
    raise Exception('Module version must follow semantic versioning format (e.g. v1.0.0)')

setup(
    name='wallaby_data_access',
    version=match.group(),
    description='Module for accessing WALLABY internal release data ',
    url='https://github.com/AusSRC/WALLABY_data_access',
    author='Austin Shen',
    author_email='austin.shen@csiro.au',
    packages=['wallaby_data_access'],
    install_requires=[
        'numpy',
        'astropy',
        'astroquery',
        'matplotlib',
        'django',
        'django_extensions',
        'psycopg2-binary',
        'python-dotenv'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3',
    ]
)
