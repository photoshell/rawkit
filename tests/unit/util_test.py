import mock
import pytest

from rawkit.util import discover


@pytest.yield_fixture
def mock_libraw():
    with mock.patch('rawkit.util.libraw') as libraw:
        yield libraw


def test_discover(mock_libraw):
    with mock.patch(
        'rawkit.util.os.walk',
        return_value=(('', None, ('foo.CR2', 'foo.jpg')),)
    ):
        mock_libraw.libraw_open_file.side_effect = [0, 1]
        files = discover('')
        assert files == ['foo.CR2'.encode('ascii')]
