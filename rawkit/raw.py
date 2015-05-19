""":mod:`rawkit.raw` --- High-level raw file API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from rawkit.libraw import libraw


class Raw(object):

    """
    Represents a raw file (of any format) and exposes development options to
    the user.

    For example, the basic workflow (open a file, process the file, save the
    file) looks like this::

        from rawkit.raw import Raw

        with Raw(filename='some/raw/image.CR2') as raw:
            raw.process()
            raw.save(filename='some/destination/image.ppm')

    :param filename: the name of a raw file to load
    :type filename: :class:`basestring`
    :returns: A raw object
    :rtype: :class:`Raw`
    """

    def __init__(self, filename=None):
        """Initializes a new Raw object."""
        self.data = libraw.libraw_init(0)
        libraw.libraw_open_file(self.data, bytes(filename, 'utf-8'))

    def __enter__(self):
        """Return a Raw object for use in context managers."""
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
        """
        Save the raw data as a new PPM or TIFF image. This method is provided
        for convenience, but in general export should actually be handled by
        another library (such as Wand).

        Keyword arguments:
        filename -- A filename (ending in ``.ppm`` or ``.tiff``) to save.
        """
        libraw.libraw_dcraw_ppm_tiff_writer(
            self.data, bytes(filename, 'utf-8'))
