import pytest

from libraw.bindings import LibRaw
from libraw.errors import UnspecifiedError


def test_check_call_success():
    LibRaw.check_call(0, None, None)


def test_check_call_error():
    with pytest.raises(UnspecifiedError):
        LibRaw.check_call(-1, None, None)
