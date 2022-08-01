import io
import os


def _write_bytesio_to_file(filename, bytesio):
    """Write the contents of the given BytesIO to a file.
    Creates the file or overwrites the file if it does
    not exist yet.

    """
    with open(filename, "wb") as outfile:
        # Copy the BytesIO stream to the output file
        outfile.write(bytesio.getbuffer())


def _write_zipped_fits_file(filename, product, compress=True):
    """Compress a .fits file as .fits.gz for a data product.

    """
    with io.BytesIO() as buf:
        buf.write(product)
        buf.seek(0)
        if not os.path.isfile(filename):
            _write_bytesio_to_file(filename, buf)
            if compress:
                os.system(f'gzip {filename}')


def _write_products(products, prefix):
    _write_zipped_fits_file('%s_cube.fits' % (prefix), products.cube)
    _write_zipped_fits_file('%s_chan.fits' % (prefix), products.chan)
    _write_zipped_fits_file('%s_mask.fits' % (prefix), products.mask)
    _write_zipped_fits_file('%s_mom0.fits' % (prefix), products.mom0)
    _write_zipped_fits_file('%s_mom1.fits' % (prefix), products.mom1)
    _write_zipped_fits_file('%s_mom2.fits' % (prefix), products.mom2)

    # Open spectrum
    with io.BytesIO() as buf:
        buf.write(b''.join(products.spec))
        buf.seek(0)
        spec_file = '%s_spec.txt' % (prefix)
        if not os.path.isfile(spec_file):
            _write_bytesio_to_file(spec_file, buf)
