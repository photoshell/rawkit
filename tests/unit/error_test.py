import pytest

from rawkit.errors import check_call
from rawkit.errors import LibrawUnspecifiedError


def test_check_call_success():
    check_call(0)


def test_check_call_error():
    with pytest.raises(LibrawUnspecifiedError):
        check_call(-1)
