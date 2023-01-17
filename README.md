# WALLABY data access

Python module with tools for accessing internal release data from the WALLABY database

## Configuration

There are two requirements for accessing data via the module. They are:

1. Clone of [WALLABY_database](https://github.com/AusSRC/WALLABY_database) repository
2. Environment file with database credentials.

The `.env` file requires:

```
DATABASE_HOST
DATABASE_NAME
DATABASE_USER
DATABASE_PASS
```

Once these files are in your working directory you can specify them in the `connect()` function

```
import wallaby_data_access as wallaby
wallaby.connect(db='<PATH_TO_WALLABY_database>', env='<PATH_TO_.env>')
```

## Testing

Inside the [`tests`](tests/) subdirectory we have files for testing the source code, and a [`Dockerfile`](tests/Dockerfile). The Dockerfile is used to create the image that is run in through Github Actions (pre-installed with the `WALLABY_database`) repository cloned.

## Release

[Official PyPI package](https://pypi.org/project/wallaby-data-access/)

We can release to PyPI manually or automatically through our [action](.github/workflows/pypi.yml). To release manually:

```
export RELEASE_VERSION=<version>
python setup.py sdist
twine upload dist/*
```
