import mock
import pytest

from rawkit import util


@pytest.yield_fixture
def mock_libraw():
    with mock.patch('rawkit.util._libraw') as libraw:
        yield libraw


def test_discover(mock_libraw):
    with mock.patch(
        'rawkit.util.os.walk',
        return_value=(('', None, ('foo.CR2', 'foo.jpg')),)
    ):
        mock_libraw.libraw_open_file.side_effect = [0, 1]
        files = util.discover('')
        assert files == ['foo.CR2'.encode('ascii')]


def test_camera_list(mock_libraw):
    with mock.patch(
        'rawkit.util._libraw.libraw_cameraCount',
        return_value=0
    ):
        assert util.camera_list() == []
        mock_libraw.libraw_cameraList.assert_called_once_with()
