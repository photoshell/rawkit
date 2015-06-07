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

    def __init__(self):  # pragma: no cover
        # TODO: This hack is required because Travis doesn't have libraw10
        try:
            super(LibRaw, self).__init__(util.find_library('raw'))
            self.libraw_init.restype = POINTER(libraw_data_t)
            self.libraw_dcraw_make_mem_image.restype = POINTER(
                libraw_processed_image_t
            )
        except:
            super(LibRaw, self).__init__(util.find_library(''))

    @property
    def version_number(self):
        """
        A numeric representation of the version of LibRaw which we have linked
        against. eg. ::

            (0, 16, 1)

        :returns: The version number
        :rtype: :class:`3 tuple`
        """
        self.libraw_version.restype = c_char_p
        v = self.libraw_versionNumber()
        print(v)
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
        self.libraw_version.restype = c_char_p
        return self.libraw_version().decode('utf-8')

    def __getitem__(self, name):
        if name.startswith('libraw_'):
            # func = self._FuncPtr((name, self))
            func = super(LibRaw, self).__getitem__(name)
            # func.__name__ = name

            errexcludes = ('libraw_cameraCount', 'libraw_versionNumber',
                           'libraw_init', 'libraw_version')

            if name not in errexcludes:
                func.errcheck = LibRaw.check_call

            # return func
            return func
