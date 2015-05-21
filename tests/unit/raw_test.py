import mock
import pytest
from rawkit.raw import Raw


@pytest.yield_fixture
def mock_libraw():
    with mock.patch('rawkit.raw.libraw') as libraw:
        yield libraw


@pytest.fixture
def input_file():
    return 'potato_salad.CR2'


@pytest.fixture
def output_file():
    return 'potato_salad.out'


def test_create(mock_libraw, input_file):
    with Raw(filename=input_file) as raw:
        mock_libraw.libraw_init.assert_called_once()
        mock_libraw.libraw_open_file.assert_called_once_with(
            raw.data,
            input_file.encode('ascii'),
        )

    mock_libraw.libraw_close.assert_called_once_with(raw.data)


def test_process(mock_libraw, input_file):
    with Raw(filename=input_file) as raw:
        raw.process()

    mock_libraw.libraw_unpack.assert_called_once_with(raw.data)
    mock_libraw.libraw_dcraw_process.assert_called_once_with(raw.data)


def _test_save(mock_libraw, input_file, output_file, filetype):
    with Raw(filename=input_file) as raw:
        raw.process()
        raw.save(filename=output_file, filetype=filetype)

    mock_libraw.libraw_dcraw_ppm_tiff_writer.assert_called_once_with(
        raw.data,
        output_file.encode('ascii'),
    )


def test_save_ppm(mock_libraw, input_file, output_file):
    _test_save(mock_libraw, input_file, output_file, 'ppm')


def test_save_tiff(mock_libraw, input_file, output_file):
    _test_save(mock_libraw, input_file, output_file, 'tiff')


def test_save_invalid(mock_libraw, input_file, output_file):
    with pytest.raises(AssertionError):
        _test_save(mock_libraw, input_file, output_file, 'jpg')


def test_to_buffer(mock_libraw, input_file):
    with Raw(filename=input_file) as raw:
        raw.process()
        # Quick hack because to_buffer does some ctypes acrobatics
        with mock.patch('rawkit.raw.ctypes'):
            raw.to_buffer()

    mock_libraw.libraw_dcraw_make_mem_image.assert_called_once_with(
        raw.data,
    )

    mock_libraw.libraw_dcraw_clear_mem.assert_called_once_with(
        mock_libraw.libraw_dcraw_make_mem_image(raw.data),
    )
