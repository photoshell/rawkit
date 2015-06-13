import ctypes
import mock
import pytest

from libraw.bindings import LibRaw
from libraw.errors import c_error, check_call, UnspecifiedError


@pytest.yield_fixture
def libraw():
    with mock.patch.object(LibRaw, '__init__', mock.Mock(return_value=None)):
        yield LibRaw()


@pytest.fixture
def error_func():
    m = mock.Mock()
    m.restype = c_error
    return m


@pytest.fixture
def int_func():
    m = mock.Mock()
    m.restype = ctypes.c_int
    return m


@pytest.fixture
def success_exit_code():
    m = mock.Mock()
    m.value = 0
    return m


@pytest.fixture
def undefined_exit_code():
    m = mock.Mock()
    m.value = -1
    return m


def test_libraw_sets_method_name(libraw):
    """
    Ensure that the method name is set when calling a LibRaw function.
    """

    libraw._FuncPtr = mock.Mock()
    libraw.libraw_init()

    assert libraw.libraw_init.__name__ == 'libraw_init'


def test_error_checking(libraw):
    """
    Check that libraw methods are assigned an error checker.
    """

    libraw._FuncPtr = mock.Mock()

    libraw.libraw_something()
    assert libraw.libraw_something.errcheck == check_call


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


def test_check_call_success(error_func, success_exit_code):
    """
    An error check with a return value of 0 should not raise.
    """

    check_call(success_exit_code, error_func, None)


def test_check_call_error(error_func, undefined_exit_code):
    """
    An error check with a negative error code should raise.
    """

    with pytest.raises(UnspecifiedError):
        check_call(undefined_exit_code, error_func, None)


def test_check_non_error_code_int(int_func, undefined_exit_code):
    """
    An error check to a method which does not return an error should not raise
    (even if the return value looks like an error code).
    """

    check_call(undefined_exit_code, int_func, None)
