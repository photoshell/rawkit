from rawkit.libraw import libraw


class Raw(object):

    def __init__(self, filename=None):
        self.data = libraw.libraw_init(0)
        libraw.libraw_open_file(self.data, bytes(filename, 'utf-8'))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Clean up after ourselves when leaving the context manager."""
        self.close()

    def close(self):
        """Free the underlying raw representation."""
        libraw.libraw_close(self.data)

    def process(self, options=None):
        """
        Unpack and process the raw data into something more usable.

        """

        libraw.libraw_unpack(self.data)
        libraw.libraw_dcraw_process(self.data)

    def save(self, filename=None):
        libraw.libraw_dcraw_ppm_tiff_writer(
            self.data, bytes(filename, 'utf-8'))
