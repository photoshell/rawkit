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

    @staticmethod
    def check_call(exit_code, func, arguments):
        """
        Throws a Python error which corresponds to the given LibRaw exit code.

        :param exit_code: the exit code returned by a LibRaw function
        :type exit_code: :class:`int`
        :returns: Returns :param:`exit_code` or throws an error from
                  :class:`libraw.errors`
        :rtype: :class:`type(exit_code)`
        """

        if func.restype is c_error and exit_code.value != 0:
            raise {
                -1: errors.UnspecifiedError,
                -2: errors.FileUnsupported,
                -3: errors.RequestForNonexistentImage,
                -4: errors.OutOfOrderCall,
                -5: errors.NoThumbnail,
                -6: errors.UnsupportedThumbnail,
                -7: errors.InputClosed,
                -100007: errors.InsufficientMemory,
                -100008: errors.DataError,
                -100009: errors.IOError,
                -100010: errors.CancelledByCallback,
                -100011: errors.BadCrop
            }[exit_code.value]

        return exit_code

    def __init__(self):  # pragma: no cover
        # TODO: This hack is required because Travis doesn't have libraw10
        try:
            super(LibRaw, self).__init__(util.find_library('raw'))

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
        except AttributeError:
            super(LibRaw, self).__init__(util.find_library(''))

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

        func.errcheck = LibRaw.check_call

        return func
