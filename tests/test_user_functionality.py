"""Collection of tests run to make sure the functionality in the notebooks works.

"""

import os
import shutil
import pytest
import warnings
from src import wallaby


OVERVIEW_PLOT_ID = 4713
TAG_NAME = 'NGC 5044 DR1'
SOURCE_NAME = 'WALLABY J134002-252831'


@pytest.fixture(scope="session", autouse=True)
def django_setup():
    wallaby.connect()


def test_print_tags():
    wallaby.print_tags()


def test_get_table():
    table = wallaby.get_catalog(TAG_NAME)
    assert (table is not None)
    table.sort("f_sum", reverse=True)


def test_overview_plot():
    warnings.filterwarnings("ignore")
    wallaby.overview_plot(id=OVERVIEW_PLOT_ID)


def test_save_catalog():
    filename = "%s.fits" % TAG_NAME.replace(' ', '_')
    if not os.path.exists(filename):
        wallaby.save_catalog(TAG_NAME, filename, format='fits')
    os.remove(filename)


def test_save_products():
    filename = f'{SOURCE_NAME.replace(" ", "_")}_products'
    wallaby.save_products_for_source(TAG_NAME, SOURCE_NAME)
    shutil.rmtree(filename)
