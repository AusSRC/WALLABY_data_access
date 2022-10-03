"""Collection of tests run to make sure the functionality in the notebooks works.

"""

import os
import shutil
import pytest
import warnings
from wallaby_data_access import wallaby


OVERVIEW_PLOT_ID = 4713
TAG_NAME = 'NGC 5044 DR2'
SOURCE_NAME = 'WALLABY J131858-150054'


@pytest.fixture(scope="session", autouse=True)
def django_setup():
    if 'WALLABY_DATABASE_PATH' in os.environ:
        wallaby.connect(os.environ['WALLABY_DATABASE_PATH'])
    else:
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


def test_get_slurmoutput_metadata():
    meta = wallaby.get_slurm_output(SOURCE_NAME)
    assert (meta is not None)


def test_get_beam_correction_metadata():
    used_holography = wallaby.get_primary_beam_correction_uses_holography(SOURCE_NAME)
    assert (used_holography is not None)


def test_get_kinematic_model_data():
    kin_tags = wallaby.get_kinematic_model_tags()
    assert (kin_tags is not None)

    kin_cat = wallaby.get_kinematic_model(team_release_kin=kin_tags[0])
    assert (kin_cat is not None)

    res = wallaby.get_kinematic_model(name=kin_cat[0]['name'])
    assert (res is not None)
    assert (len(res) == 1)
