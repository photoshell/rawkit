import mock

from libraw.bindings import LibRaw


def test_libraw_sets_method_name():
    libraw = LibRaw()
    libraw._FuncPtr = mock.Mock()
    libraw.libraw_init()

    assert libraw.libraw_init.__name__ == 'libraw_init'


def test_error_checking():
    """
    Check that libraw methods are assigned an error checker (unless they're on
    the white list).
    """

    libraw = LibRaw()
    libraw._FuncPtr = mock.Mock()

    libraw.libraw_cameraCount()
    assert libraw.libraw_cameraCount.errcheck != LibRaw.check_call

    libraw.libraw_init()
    assert libraw.libraw_init.errcheck == LibRaw.check_call
