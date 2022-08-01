"""Collection of tests run to make sure the functionality in the notebooks works.

"""

import pytest
from src import wallaby


TAG_NAME = 'NGC 5044 DR1'


@pytest.fixture(scope="session", autouse=True)
def django_setup():
    wallaby.connect()


def test_print_tags():
    wallaby.print_tags()


def test_get_table():
    table = wallaby.get_catalog(TAG_NAME)
    assert(table is not None)
