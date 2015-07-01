""":mod:`libraw.callbacks` --- LibRaw callback definitions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Warning:

    You will need to keep a reference to your callback functions for as long as
    you want to call them from C code, otherwise they may be garbage collected
    and lead to a segmentation fault.
"""

from ctypes import *  # noqa

memory_callback = CFUNCTYPE(c_void_p, c_char_p, c_char_p)
"""
Creates a callback for use when there are memory errors in LibRaw.

.. sourcecode:: python

    def memory_cb(data, file, where):
        pass

    cb = memory_callback(memory_cb)

    libraw.libraw_set_memerror_handler(libraw_data, cb, data)

Your callback function should map to the LibRaw C callback definition below:

.. sourcecode:: c

    typedef void (*memory_callback) (
        void *data, const char *file, const char *where
    );

Args:
    callback (function): The Python function to convert to a C callback.

Returns:
    _ctypes.PyCFuncPtrType: A C callback.
"""

data_callback = CFUNCTYPE(c_void_p, c_char_p, c_int)
"""
A callback for use when there are data errors in LibRaw.

.. sourcecode:: python

    def data_cb(data, file, offset):
        pass

    cb = data_callback(data_cb)

    libraw.libraw_set_dataerror_handler(libraw_data, cb, data)

Your callback function should map to the LibRaw C callback definition below:

.. sourcecode:: c

    typedef void (*data_callback) (
        void *data, const char *file, const int offset
    );

Args:
    callback (function): The Python function to convert to a C callback.

Returns:
    _ctypes.PyCFuncPtrType: A C callback.
"""

progress_callback = CFUNCTYPE(c_void_p, c_int, c_int, c_int)
"""
A callback that will be called to alert you to the stages of image processing.

.. sourcecode:: python

    def progress_cb(data, stage, iteration, expected):
        pass

    cb = progress_callback(progress_cb)

    libraw.libraw_set_progress_handler(libraw_data, cb, data)

Your callback function should map to the LibRaw C callback definition below:

.. sourcecode:: c

    typedef void (*progress_callback) (
        void *data, enum LibRaw_progress stage, int iterationa, int expected
    );

Args:
    callback (function): The Python function to convert to a C callback.

Returns:
    _ctypes.PyCFuncPtrType: A C callback.
"""
