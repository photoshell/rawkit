""":mod:`libraw.bindings` --- Low-level LibRaw bindings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :class:`libraw.bindings` module handles linking against the LibRaw binary.
It does not provide an API.
"""

from ctypes import *  # noqa
from ctypes import util

from libraw.structs import libraw_data_t, libraw_processed_image_t

# TODO: This is necessary because Travis CI is still using Ubuntu 12.04
try:
    # TODO: This will do bad things if the API version isn't 10
    libraw = cdll.LoadLibrary(util.find_library('raw'))    # pragma: no cover
    libraw.libraw_init.restype = POINTER(libraw_data_t)    # pragma: no cover
    libraw.libraw_dcraw_make_mem_image.restype = POINTER(  # pragme: no cover
        libraw_processed_image_t                           # pragma: no cover
    )                                                      # pragma: no cover
except:                                                    # pragma: no cover
    libraw = cdll.LoadLibrary('')                          # pragma: no cover
