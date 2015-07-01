import mock
import pytest

from rawkit import util
from libraw.errors import FileUnsupported


@pytest.yield_fixture
def libraw():
    with mock.patch('rawkit.util.LibRaw') as libraw:
        # TODO: There must be a better way...
        libraw.return_value = libraw
        yield libraw


def test_discover(libraw):
    with mock.patch(
        'rawkit.util.os.walk',
        return_value=(('', None, ('foo.CR2', 'foo.jpg')),)
    ):
        libraw.libraw_open_file.side_effect = [0, FileUnsupported()]
        files = util.discover('')
        assert files == ['foo.CR2'.encode('ascii')]


def test_camera_list(libraw):
    libraw.libraw_cameraCount.return_value = 0
    assert util.camera_list() == []
    libraw.libraw_cameraList.assert_called_once_with()
