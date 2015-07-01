""":mod:`rawkit.raw` --- High-level raw file API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import ctypes
import os
import random
import string
import tempfile

from rawkit.errors import NoFileSpecified, InvalidFileType
from libraw.bindings import LibRaw

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

    Args:
        filename (str): The name of a raw file to load.

    Returns:
        Raw: A raw object.

    Raises:
        rawkit.errors.NoFileSpecified: If `filename` is ``None``.
    """

    def __init__(self, filename=None):
        """Initializes a new Raw object."""
        if filename is None:
            raise NoFileSpecified()
        self.libraw = LibRaw()
        self.data = self.libraw.libraw_init(0)
        self.libraw.libraw_open_file(self.data, filename.encode('ascii'))

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
        self.libraw.libraw_close(self.data)

    def unpack(self):
        """Unpack the raw data."""
        if not self.image_unpacked:
            self.libraw.libraw_unpack(self.data)
            self.image_unpacked = True

    def unpack_thumb(self):
        """Unpack the thumbnail data."""
        if not self.thumb_unpacked:
            self.libraw.libraw_unpack_thumb(self.data)
            self.thumb_unpacked = True

    def process(self):
        """Process the raw data based on self.options"""
        self.options._map_to_libraw_params(self.data.contents.params)
        self.libraw.libraw_dcraw_process(self.data)

    def save(self, filename=None, filetype='ppm'):
        """
        Save the image data as a new PPM or TIFF image.

        Args:
            filename (str): The name of an image file to save.
            filetype (str): The type of file to output (``ppm`` or ``tiff``).

        Raises:
            rawkit.errors.NoFileSpecified: If `filename` is ``None``.
            rawkit.errors.InvalidFileTypeError: If `filetype` is not ``ppm`` or
                ``tiff``.
        """
        if filename is None:
            raise NoFileSpecified()
        if filetype not in ('ppm', 'tiff'):
            raise InvalidFileType('Output filetype must be "ppm" or "tiff"')
        self.data.contents.params.output_tiff = 0 if filetype is 'ppm' else 1

        self.unpack()
        self.process()

        self.libraw.libraw_dcraw_ppm_tiff_writer(
            self.data, filename.encode('ascii'))

    def save_thumb(self, filename=None):
        """
        Save the thumbnail data.

        Args:
            filename (str): The name of an image file to save.

        Raises:
            rawkit.errors.NoFileSpecified: If `filename` is ``None``.
        """
        if filename is None:
            raise NoFileSpecified()

        self.unpack_thumb()

        self.libraw.libraw_dcraw_thumb_writer(
            self.data, filename.encode('ascii'))

    def to_buffer(self):
        """
        Convert the image to an RGB buffer.

        Returns:
            bytearray: RGB data of the image.
        """
        self.unpack()
        self.process()

        processed_image = self.libraw.libraw_dcraw_make_mem_image(self.data)
        data_pointer = ctypes.cast(
            processed_image.contents.data,
            ctypes.POINTER(ctypes.c_byte * processed_image.contents.data_size)
        )
        data = bytearray(data_pointer.contents)
        self.libraw.libraw_dcraw_clear_mem(processed_image)

        return data

    def thumbnail_to_buffer(self):
        """
        Convert the thumbnail data as an RGB buffer.

        Returns:
            bytearray: RGB data of the thumbnail.
        """
        self.unpack_thumb()

        processed_image = self.libraw.libraw_dcraw_make_mem_thumb(self.data)
        data_pointer = ctypes.cast(
            processed_image.contents.data,
            ctypes.POINTER(ctypes.c_byte * processed_image.contents.data_size)
        )
        data = bytearray(data_pointer.contents)
        self.libraw.libraw_dcraw_clear_mem(processed_image)

        return data

    @property
    def metadata(self):
        """
        Common metadata for the photo

        Returns:
            rawkit.metadata.Metadata: A metadata object.
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


class DarkFrame(Raw):

    """
    Represents a dark frame---a raw photo taken in low light which can be
    subtracted from another photos raw data.

    Creates a temporary file which is not cleaned up until the dark frame is
    closed.
    """

    def __init__(self, filename=None):
        """Initializes a new DarkFrame object."""
        super(DarkFrame, self).__init__(filename=filename)
        self.options = Options({
            'auto_brightness': False,
            'brightness': 1.0,
            'auto_stretch': True,
            'bps': 16,
            'gamma': (1, 1),
            'rotation': 0,
        })
        self._tmp = os.path.join(
            tempfile.gettempdir(),
            '{prefix}{rand}'.format(
                prefix=tempfile.gettempprefix(),
                rand=''.join(random.SystemRandom().choice(
                    string.ascii_uppercase + string.digits) for _ in range(8)
                )
            )
        )
        self._filetype = None

    def save(self, filename=None, filetype='ppm'):
        """
        Save the image data, defaults to using a temp file.

        Args:
            filename (str): The name of an image file to save.
            filetype (str): The type of file to output (``ppm`` or ``tiff``).

        Raises:
            rawkit.errors.InvalidFileTypeError: If `filetype` is not ``ppm`` or
                ``tiff``.
        """

        if filename is None:
            filename = self._tmp

        if not os.path.isfile(filename):
            super(DarkFrame, self).save(filename=filename, filetype=filetype)

    @property
    def name(self):
        """
        A tempfile in a unique directory.

        Returns:
            str: The name of a temp file.
        """
        return self._tmp

    def cleanup(self):
        """Cleanup temp files."""
        try:
            os.unlink(self._tmp)
        except OSError:
            pass

    def close(self):
        """Free the underlying raw representation and cleanup temp files."""
        super(DarkFrame, self).close()
        self.cleanup()
