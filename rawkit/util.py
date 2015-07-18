""":mod:`rawkit.util` --- Utility functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These functions perform helpful tasks which don't really fit anywhere else such
as searching for Raw files on the disk, or checking what cameras are supported
by LibRaw.
"""

import ctypes
import os

from libraw.bindings import LibRaw
from libraw.errors import FileUnsupported


def discover(path):
    """
    Recursively search for raw files in a given directory.

    Args:
        path (str): A tree to recursively search.
    """
    file_list = []
    libraw = LibRaw()
    raw = libraw.libraw_init(0)

    for root, _, files in os.walk(path):
        for file_name in files:
            file_path = os.path.join(root, file_name).encode('ascii')
            try:
                libraw.libraw_open_file(raw, file_path)
            except FileUnsupported:
                continue
            finally:
                libraw.libraw_recycle(raw)
            file_list.append(file_path)

    libraw.libraw_close(raw)
    return file_list


def camera_list():
    """
    Return a list of cameras which are supported by the currently linked
    version of LibRaw.

    Returns:
        str array: A list of supported cameras.
    """

    libraw = LibRaw()
    libraw.libraw_cameraList.restype = ctypes.POINTER(
        ctypes.c_char_p * libraw.libraw_cameraCount()
    )
    data_pointer = libraw.libraw_cameraList()
    return [x.decode('ascii') for x in data_pointer.contents]
