""":mod:`libraw.callbacks` --- LibRaw callback definitions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Note that you will need to keep a reference to your callback functions for as
long as you want to call them from C code, otherwise they may be garbage
collected and lead to a segmentation fault.
"""

from ctypes import *  # noqa

exif_parser_callback = CFUNCTYPE(
    c_void_p, c_int, c_int, c_int, c_int, c_void_p
)
"""
Creates a callback for use by the EXIF parser.

.. sourcecode:: python

    def exif_cb(context, tag, type, len, ord, ifp):
        pass

    cb = CFUNCTYPE(exif_cb)

    libraw.libraw_set_exifparser_handler(libraw_data, cb, data)

Your callback function should map to the LibRaw C callback definition below:

.. sourcecode:: c

    typedef void (*exif_parser_callback) (
        void *context, int tag, int type, int len, unsigned int ord, void *ifp
    );

:param callback: the Python function to convert to a C callback.
:type callback: :class:`function`
:returns: A C callback
:rtype: :class:`_ctypes.PyCFuncPtrType`
"""

memory_callback = CFUNCTYPE(c_void_p, c_char_p, c_char_p)
"""
Creates a callback for use when there are memory errors in LibRaw.

.. sourcecode:: python

    def memory_cb(data, file, where):
        pass

    cb = CFUNCTYPE(memory_cb)

    libraw.libraw_set_memerror_handler(libraw_data, cb, data)

Your callback function should map to the LibRaw C callback definition below:

.. sourcecode:: c

    typedef void (*memory_callback) (
        void *data, const char *file, const char *where
    );

:param callback: the Python function to convert to a C callback.
:type callback: :class:`function`
:returns: A C callback
:rtype: :class:`_ctypes.PyCFuncPtrType`
"""

data_callback = CFUNCTYPE(c_void_p, c_char_p, c_int)
"""
A callback for use when there are data errors in LibRaw.

.. sourcecode:: python

    def data_cb(data, file, offset):
        pass

    cb = CFUNCTYPE(data_cb)

    libraw.libraw_set_dataerror_handler(libraw_data, cb, data)

Your callback function should map to the LibRaw C callback definition below:

.. sourcecode:: c

    typedef void (*data_callback) (
        void *data, const char *file, const int offset
    );

:param callback: the Python function to convert to a C callback.
:type callback: :class:`function`
:returns: A C callback
:rtype: :class:`_ctypes.PyCFuncPtrType`
"""

progress_callback = CFUNCTYPE(c_void_p, c_int, c_int, c_int)
"""
A callback that will be called to alert you to the stages of image processing.

.. sourcecode:: python

    def progress_cb(data, stage, iteration, expected):
        pass

    cb = CFUNCTYPE(progress_cb)

    libraw.libraw_set_progress_handler(libraw_data, cb, data)

Your callback function should map to the LibRaw C callback definition below:

.. sourcecode:: c

    typedef void (*progress_callback) (
        void *data, enum LibRaw_progress stage, int iterationa, int expected
    );

:param callback: the Python function to convert to a C callback.
:type callback: :class:`function`
:returns: A C callback
:rtype: :class:`_ctypes.PyCFuncPtrType`
"""
