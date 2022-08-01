"""Collection of tests run to make sure the functionality in the notebooks works.

"""

import pytest
from src import wallaby


@pytest.fixture(scope="session", autouse=True)
def django_setup():
    wallaby.connect()


def test_print_tags():
    wallaby.print_tags()
