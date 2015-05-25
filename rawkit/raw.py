""":mod:`rawkit.raw` --- High-level raw file API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import ctypes

from rawkit.libraw import libraw
from rawkit.metadata import Metadata
from rawkit.options import Options


class Raw(object):

    """
    Represents a raw file (of any format) and exposes development options to
    the user.

    For example, the basic workflow (open a file, process the file, save the
    file) looks like this::

        from rawkit.raw import Raw
        from rawkit.options import WhiteBalance

        with Raw(filename='some/raw/image.CR2') as raw:
            raw.options.white_balance = WhiteBalance(camera=False, auto=True)
            raw.save(filename='some/destination/image.ppm')

    :param filename: the name of a raw file to load
    :type filename: :class:`basestring`
    :returns: A raw object
    :rtype: :class:`Raw`
    """

    def __init__(self, filename=None):
        """Initializes a new Raw object."""
        self.data = libraw.libraw_init(0)
        libraw.libraw_open_file(self.data, filename.encode('ascii'))

        self.options = Options()

        self.image_unpacked = False
        self.thumb_unpacked = False

    def __enter__(self):
        """Return a Raw object for use in context managers."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Clean up after ourselves when leaving the context manager."""
        self.close()

    def close(self):
        """Free the underlying raw representation."""
        libraw.libraw_close(self.data)

    def unpack(self):
        """Unpack the raw data."""
        if not self.image_unpacked:
            libraw.libraw_unpack(self.data)
            self.image_unpacked = True

    def unpack_thumb(self):
        """Unpack the thumbnail data."""
        if not self.thumb_unpacked:
            libraw.libraw_unpack_thumb(self.data)
            self.thumb_unpacked = True

    def process(self):
        """Process the raw data based on self.options"""
        self.options._map_to_libraw_params(self.data.contents.params)
        libraw.libraw_dcraw_process(self.data)

    def save(self, filename=None, filetype='ppm'):
        """
        Save the image data as a new PPM or TIFF image.

        :param filename: the name of an image file to save
        :type filename: :class:`basestring`
        :param filetype: the type of file to output (``ppm`` or ``tiff``)
        :type filetype: :class:`basestring`
        """
        assert filetype in ('ppm', 'tiff')
        self.data.contents.params.output_tiff = 0 if filetype is 'ppm' else 1

        self.unpack()
        self.process()

        libraw.libraw_dcraw_ppm_tiff_writer(
            self.data, filename.encode('ascii'))

    def save_thumb(self, filename=None):
        """
        Save the thumbnail data.

        :param filename: the name of an image file to save
        :type filename: :class:`basestring`
        """
        self.unpack_thumb()

        libraw.libraw_dcraw_thumb_writer(
            self.data, filename.encode('ascii'))

    def to_buffer(self):
        """
        Return the image data as an RGB buffer.

        :returns: RGB data of the image
        :rtype: :class:`bytearray`
        """
        self.unpack()
        self.process()

        processed_image = libraw.libraw_dcraw_make_mem_image(self.data)
        data_pointer = ctypes.cast(
            processed_image.contents.data,
            ctypes.POINTER(ctypes.c_byte * processed_image.contents.data_size)
        )
        data = bytearray(data_pointer.contents)
        libraw.libraw_dcraw_clear_mem(processed_image)

        return data

    def thumbnail_to_buffer(self):
        """
        Return the thumbnail data as an RGB buffer.

        :returns: RGB data of the thumbnail
        :rtype: :class:`bytearray`
        """
        self.unpack_thumb()

        processed_image = libraw.libraw_dcraw_make_mem_thumb(self.data)
        data_pointer = ctypes.cast(
            processed_image.contents.data,
            ctypes.POINTER(ctypes.c_byte * processed_image.contents.data_size)
        )
        data = bytearray(data_pointer.contents)
        libraw.libraw_dcraw_clear_mem(processed_image)

        return data

    @property
    def metadata(self):
        """
        Common metadata for the photo

        :returns: A metadata object
        :rtype: :class:`~rawkit.metadata.Metadata`
        """
        return Metadata(
            aperture=self.data.contents.other.aperture,
            timestamp=self.data.contents.other.timestamp,
            shutter=self.data.contents.other.shutter,
            flash=bool(self.data.contents.color.flash_used),
            focal_length=self.data.contents.other.focal_len,
            height=self.data.contents.sizes.height,
            iso=self.data.contents.other.iso_speed,
            make=self.data.contents.idata.make,
            model=self.data.contents.idata.model,
            orientation=self.data.contents.sizes.flip,
            width=self.data.contents.sizes.width,
        )
