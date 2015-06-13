""":mod:`libraw.bindings` --- Low-level LibRaw bindings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :class:`libraw.bindings` module handles linking against the LibRaw binary.
"""

from ctypes import *  # noqa
from ctypes import util

from libraw import errors
from libraw.errors import c_error
from libraw.structs import libraw_data_t, libraw_processed_image_t


class LibRaw(CDLL):

    """
    A :class:`ctypes.CDLL` that links against `libraw.so` (or the equivalent on
    your platform).
    """

    def __init__(self):  # pragma: no cover
        libraw = util.find_library('raw')
        try:
            if libraw is not None:
                super(LibRaw, self).__init__(libraw)
            else:
                raise ImportError
        except (ImportError, AttributeError, OSError, IOError):
            raise ImportError('Cannot find LibRaw on your system!')

        # Define return types

        self.libraw_init.restype = POINTER(libraw_data_t)
        self.libraw_version.restype = c_char_p
        self.libraw_strprogress.restype = c_char_p
        self.libraw_versionNumber.restype = c_int
        self.libraw_cameraCount.restype = c_int
        self.libraw_cameraList.restype = POINTER(
            c_char_p * self.libraw_cameraCount()
        )
        self.libraw_unpack_function_name.restype = c_char_p
        self.libraw_subtract_black.restype = POINTER(libraw_data_t)
        self.libraw_open_file.restype = c_error
        self.libraw_open_file_ex.restype = c_error
        self.libraw_open_buffer.restype = c_error
        self.libraw_unpack.restype = c_error
        self.libraw_unpack_thumb.restype = c_error
        self.libraw_adjust_sizes_info_only.restype = c_error
        self.libraw_dcraw_ppm_tiff_writer.restype = c_error
        self.libraw_dcraw_thumb_writer.restype = c_error
        self.libraw_dcraw_process.restype = c_error
        self.libraw_dcraw_make_mem_image.restype = POINTER(
            libraw_processed_image_t)
        self.libraw_dcraw_make_mem_thumb.restype = POINTER(
            libraw_processed_image_t)
        self.libraw_raw2image.restype = c_error
        self.libraw_get_decoder_info.restype = c_error
        self.libraw_COLOR.restype = c_error
        try:
            self.libraw_open_wfile.restype = c_error
            self.libraw_open_wfile_ex.restype = c_error
        except AttributeError:
            pass

    @property
    def version_number(self):
        """
        A numeric representation of the version of LibRaw which we have linked
        against in ``(Major, Minor, Patch)`` form. eg. ::

            (0, 16, 1)

        :returns: The version number
        :rtype: :class:`3 tuple`
        """
        v = self.libraw_versionNumber()
        return ((v >> 16) & 0x0000ff, (v >> 8) & 0x0000ff, v & 0x0000ff)

    @property
    def version(self):
        """
        A string representation of the version of LibRaw which we have linked
        against. eg. ::

            "0.16.1-Release"

        :returns: The version
        :rtype: :class:`basestring`
        """
        return self.libraw_version().decode('utf-8')

    def __getitem__(self, name):
        func = super(LibRaw, self).__getitem__(name)

        func.errcheck = errors.check_call

        return func
