import pytest

from libraw.errors import check_call
from libraw.errors import UnspecifiedError


def test_check_call_success():
    check_call(0)


def test_check_call_error():
    with pytest.raises(UnspecifiedError):
        check_call(-1)
