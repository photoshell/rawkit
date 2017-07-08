""":mod:`libraw.bindings` --- Low-level LibRaw bindings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :class:`libraw.bindings` module handles linking against the LibRaw binary.
"""

from ctypes import *  # noqa
from ctypes import util

from libraw import errors
from libraw.callbacks import data_callback
from libraw.callbacks import memory_callback
from libraw.callbacks import progress_callback
from libraw.errors import c_error
from libraw import structs_16
from libraw import structs_17
from libraw import structs_18


class LibRaw(CDLL):

    """
    A :class:`ctypes.CDLL` that links against `libraw.so` (or the equivalent on
    your platform).

    Raises:
        ImportError: If LibRaw cannot be found on your system, or linking
                     fails.
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

        try:
            structs = {
                16: structs_16,
                17: structs_17,
                18: structs_18,
            }[self.version_number[1]]
        except KeyError:
            raise ImportError(
                'Unsupported Libraw version: %s.%s.%s.' % self.version_number
            )

        libraw_data_t = structs.libraw_data_t
        libraw_decoder_info_t = structs.libraw_decoder_info_t
        libraw_processed_image_t = structs.libraw_processed_image_t

        # Define arg types

        self.libraw_init.argtypes = [c_int]
        # enum LibRaw_progress
        self.libraw_strprogress.argtypes = [c_int]
        self.libraw_unpack_function_name.argtypes = [POINTER(libraw_data_t)]

        self.libraw_subtract_black.argtypes = [POINTER(libraw_data_t)]
        self.libraw_open_file.argtypes = [POINTER(libraw_data_t), c_char_p]
        self.libraw_open_file_ex.argtypes = [
            POINTER(libraw_data_t),
            c_char_p,
            c_int64
        ]
        self.libraw_open_buffer.argtypes = [
            POINTER(libraw_data_t),
            c_void_p,
            c_int64
        ]
        self.libraw_unpack.argtypes = [POINTER(libraw_data_t)]
        self.libraw_unpack_thumb.argtypes = [POINTER(libraw_data_t)]
        self.libraw_recycle_datastream.argtypes = [POINTER(libraw_data_t)]
        self.libraw_recycle.argtypes = [POINTER(libraw_data_t)]
        self.libraw_close.argtypes = [POINTER(libraw_data_t)]
        self.libraw_set_memerror_handler.argtypes = [
            POINTER(libraw_data_t),
            memory_callback,
            c_void_p,
        ]
        self.libraw_set_dataerror_handler.argtypes = [
            POINTER(libraw_data_t),
            data_callback,
            c_void_p,
        ]
        self.libraw_set_progress_handler.argtypes = [
            POINTER(libraw_data_t),
            progress_callback,
            c_void_p,
        ]
        self.libraw_adjust_sizes_info_only.argtypes = [
            POINTER(libraw_data_t)
        ]
        self.libraw_dcraw_ppm_tiff_writer.argtypes = [
            POINTER(libraw_data_t),
            c_char_p
        ]
        self.libraw_dcraw_thumb_writer.argtypes = [
            POINTER(libraw_data_t),
            c_char_p
        ]
        self.libraw_dcraw_process.argtypes = [POINTER(libraw_data_t)]
        self.libraw_dcraw_make_mem_image.argtypes = [
            POINTER(libraw_data_t),
            POINTER(c_int)
        ]
        self.libraw_dcraw_make_mem_thumb.argtypes = [
            POINTER(libraw_data_t),
            POINTER(c_int)
        ]
        self.libraw_dcraw_clear_mem.argtypes = [
            POINTER(libraw_processed_image_t)
        ]
        self.libraw_raw2image.argtypes = [POINTER(libraw_data_t)]
        self.libraw_free_image.argtypes = [POINTER(libraw_data_t)]
        self.libraw_get_decoder_info.argtypes = [
            POINTER(libraw_data_t),
            POINTER(libraw_decoder_info_t)
        ]
        self.libraw_COLOR.argtypes = [
            POINTER(libraw_data_t),
            c_int,
            c_int
        ]

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
        self.libraw_COLOR.restype = c_int

        # Some special Windows-only garbage:

        try:
            self.libraw_open_wfile.argtypes = [
                POINTER(libraw_data_t),
                c_wchar_p
            ]
            self.libraw_open_wfile_ex.argtypes = [
                POINTER(libraw_data_t),
                c_wchar_p,
                c_int64
            ]
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

        Returns:
            3 tuple: The version number
        """
        v = self.libraw_versionNumber()
        return ((v >> 16) & 0x0000ff, (v >> 8) & 0x0000ff, v & 0x0000ff)

    @property
    def version(self):
        """
        A string representation of the version of LibRaw which we have linked
        against. eg. ::

            "0.16.1-Release"

        Returns:
            str: The version
        """
        return self.libraw_version().decode('utf-8')

    def __getitem__(self, name):
        func = super(LibRaw, self).__getitem__(name)

        func.errcheck = errors.check_call

        return func
