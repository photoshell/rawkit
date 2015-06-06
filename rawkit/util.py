import ctypes
import os

from libraw import libraw


def discover(path):
    """
    Recursively search for raw files in a given directory.
    :param path: the directory to recursively search
    :type path: :class:`basestring`
    """
    file_list = []
    raw = libraw.libraw_init(0)

    for root, _, files in os.walk(path):
        for file_name in files:
            file_path = os.path.join(root, file_name).encode('ascii')
            if libraw.libraw_open_file(raw, file_path) == 0:
                file_list.append(file_path)
            libraw.libraw_recycle(raw)

    libraw.libraw_close(raw)
    return file_list


def camera_list():
    """
    Return a list of cameras which are supported by the currently linked
    version of LibRaw.

    :returns: A list of supported cameras
    :rtype: :class:`basestring tuple`
    """
    libraw.libraw_cameraList.restype = ctypes.POINTER(
        ctypes.c_char_p * libraw.libraw_cameraCount()
    )
    data_pointer = libraw.libraw_cameraList()
    return [x.decode('ascii') for x in data_pointer.contents]
