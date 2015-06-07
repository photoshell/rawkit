import mock
import pytest

from libraw.bindings import LibRaw


@pytest.fixture
def libraw():
    return LibRaw()


def test_libraw_sets_method_name(libraw):
    """
    Ensure that the method name is set when calling a LibRaw function.
    """

    libraw._FuncPtr = mock.Mock()
    libraw.libraw_init()

    assert libraw.libraw_init.__name__ == 'libraw_init'


def test_error_checking(libraw):
    """
    Check that libraw methods are assigned an error checker (unless they're on
    the white list).
    """

    libraw._FuncPtr = mock.Mock()

    libraw.libraw_cameraCount()
    assert libraw.libraw_cameraCount.errcheck != LibRaw.check_call

    libraw.libraw_something()
    assert libraw.libraw_something.errcheck == LibRaw.check_call


def test_version_number_calculation(libraw):
    """
    Check that the version tuple is calculated correctly.
    """

    libraw.libraw_versionNumber = lambda: 4097
    assert libraw.version_number == (0, 16, 1)


def test_version(libraw):
    """
    Check that the version method actually calls `LibRaw::version()`.
    """

    libraw.libraw_version = mock.Mock()
    libraw.version
    libraw.libraw_version.assert_called_once_with()


def test_get_non_libraw_method(libraw):
    """
    Tets getting a method from an instance of `LibRaw` that does not exist in
    the DLL (eg. that does not start with `libraw_`) and is not an instance
    method. Expected behavior is to return `None`.
    """

    assert libraw.test is None
