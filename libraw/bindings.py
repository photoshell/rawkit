""":mod:`libraw.bindings` --- Low-level LibRaw bindings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :class:`libraw.bindings` module handles linking against the LibRaw binary.
It does not provide an API.
"""

from ctypes import *  # noqa
from ctypes import util

from libraw import errors
from libraw.structs import libraw_data_t, libraw_processed_image_t


class LibRaw(CDLL):

    """
    A :class:`ctypes.CDLL` that loads an instance of `libraw.so` (or the
    equivalent on your platform).
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

        if isinstance(exit_code, int) and exit_code is not 0:
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
            }[exit_code]

        return exit_code

    def __init__(self):
        super(LibRaw, self).__init__(util.find_library('raw'))
        self.libraw_init.restype = POINTER(libraw_data_t)
        self.libraw_dcraw_make_mem_image.restype = POINTER(
            libraw_processed_image_t
        )

    def __getitem__(self, name):
        func = self._FuncPtr((name, self))
        func.__name__ = name
        func.errcheck = LibRaw.check_call

        return func
