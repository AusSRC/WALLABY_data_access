#!/usr/bin/env python3
"""
Test code in cells of user download notebook.
"""

import os
import shutil
import pytest
import warnings
from wallaby_data_access import wallaby


OVERVIEW_PLOT_ID = 4713
TAG_NAME = 'NGC 5044 DR2'
KIN_TAG_NAME = "NGC 5044 Kin TR1"
SOURCE_NAME = 'WALLABY J131858-150054'


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


def test_download_catalog():
    filename = "%s.fits" % TAG_NAME.replace(' ', '_')
    table = wallaby.get_catalog(TAG_NAME)
    table['comments'] = [''.join(comment) for comment in table['comments']]
    table['tags'] = [''.join(t) for t in table['tags']]
    table.write(filename, format='fits')
    os.remove(filename)


def test_download_products():
    table = wallaby.get_catalog(TAG_NAME)
    row = table[0]
    source_id = int(row['id'])
    filename = f'{SOURCE_NAME.replace(" ", "_")}_{TAG_NAME}_products'
    wallaby.save_products_for_source(source_id, filename)

    # TODO: do we want to include the tests below?
    # Test output product names include tag and source name
    # product_files = glob.glob(f'{filename}/*.fits*', recursive=True)
    # for f in product_files:
    #     basename = os.path.basename(f)
    #     assert (row['name'].replace(' ', '_') in basename)
    #     assert (TAG_NAME in basename)
    shutil.rmtree(filename)


def test_get_kinematic_model_tags():
    wallaby.get_kinematic_model_tags()


def test_write_kinematic_model_table():
    kin_table = wallaby.get_kinematic_model(team_release_kin=KIN_TAG_NAME)
    assert (kin_table is not None)

    string_array_columns = ['rad', 'vrot_model', 'e_vrot_model', 'e_vrot_model_inc', 'rad_sd', 'sd_model', 'sd_fo_model', 'e_sd_model', 'e_sd_fo_model_inc']
    filename = "%s_catalog.fits" % KIN_TAG_NAME.replace(' ', '_')
    for column in string_array_columns:
        array = kin_table[column]
        string_array = []
        for elem in array:
            string_elem = ','.join([str(v) for v in list(elem)])
            string_array.append(string_elem)
        kin_table[column] = string_array

    kin_table.write(filename, format='fits')
    assert (os.path.exists(filename))
    os.remove(filename)


def test_write_kinematic_model_products():
    kin_table = wallaby.get_kinematic_model(team_release_kin=KIN_TAG_NAME)
    assert (kin_table is not None)

    # products for single kinematic model
    row = kin_table[0]
    kin_id = int(row['id'])
    name = str(row['source']).replace(' ', '_')
    filename = f'{name}_kinematic_products'
    wallaby.save_products_for_kinematic_model(kin_id, filename)
    assert (os.path.exists(filename))
    shutil.rmtree(filename)

    # products for multiple kinematic models
    filename = f"{KIN_TAG_NAME.replace(' ', '_')}_kin_products"
    wallaby.save_kinematic_model_products(kin_table[0:2], filename)
    assert (os.path.exists(filename))
    shutil.rmtree(filename)
    os.remove(filename + '.tar.gz')


def test_get_slurmoutput_metadata():
    meta = wallaby.get_slurm_output(SOURCE_NAME)
    assert (meta is not None)


def test_get_beam_correction_metadata():
    used_holography = wallaby.get_primary_beam_correction_uses_holography(SOURCE_NAME)
    assert (used_holography is not None)
