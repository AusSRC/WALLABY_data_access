import pytest
from src import wallaby


@pytest.fixture(scope="session", autouse=True)
def django_setup():
    wallaby.connect()


def test_connect():
    pass