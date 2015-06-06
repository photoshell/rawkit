import mock
import pytest
from rawkit.errors import InvalidFileType, NoFileSpecified
from rawkit.metadata import Metadata
from rawkit.raw import Raw


@pytest.yield_fixture
def mock_libraw():
    with mock.patch('rawkit.raw._libraw') as libraw:
        yield libraw


@pytest.fixture
def input_file():
    return 'potato_salad.CR2'


@pytest.fixture
def output_file():
    return 'potato_salad.out'


@pytest.yield_fixture
def raw(mock_libraw, input_file):
    with Raw(filename=input_file) as raw_obj:
        yield raw_obj
    mock_libraw.libraw_close.assert_called_once_with(raw_obj.data)


def test_create(mock_libraw, raw, input_file):
    mock_libraw.libraw_init.assert_called_once()
    mock_libraw.libraw_open_file.assert_called_once_with(
        raw.data,
        input_file.encode('ascii'),
    )


def test_create_no_filename(mock_libraw):
    with pytest.raises(NoFileSpecified):
        Raw()


def test_unpack(mock_libraw, raw):
    raw.unpack()
    mock_libraw.libraw_unpack.assert_called_once_with(raw.data)


def test_unpack_twice(mock_libraw, raw):
    raw.unpack()
    raw.unpack()
    mock_libraw.libraw_unpack.assert_called_once_with(raw.data)


def test_unpack_thumb(mock_libraw, raw):
    raw.unpack_thumb()
    mock_libraw.libraw_unpack_thumb.assert_called_once_with(raw.data)


def test_unpack_thumb_twice(mock_libraw, raw):
    raw.unpack_thumb()
    raw.unpack_thumb()
    mock_libraw.libraw_unpack_thumb.assert_called_once_with(raw.data)


def _test_save(mock_libraw, raw, output_file, filetype):
    raw.save(filename=output_file, filetype=filetype)

    mock_libraw.libraw_dcraw_ppm_tiff_writer.assert_called_once_with(
        raw.data,
        output_file.encode('ascii'),
    )


def test_save_no_filename(mock_libraw, raw):
    with pytest.raises(NoFileSpecified):
        raw.save(filetype='ppm')


def test_save_ppm(mock_libraw, raw, output_file):
    _test_save(mock_libraw, raw, output_file, 'ppm')


def test_save_tiff(mock_libraw, raw, output_file):
    _test_save(mock_libraw, raw, output_file, 'tiff')


def test_save_invalid(mock_libraw, raw, output_file):
    with pytest.raises(InvalidFileType):
        _test_save(mock_libraw, raw, output_file, 'jpg')


def test_save_thumb(mock_libraw, raw, output_file):
    raw.save_thumb(filename=output_file)

    mock_libraw.libraw_dcraw_thumb_writer.assert_called_once_with(
        raw.data,
        output_file.encode('ascii'),
    )


def test_to_buffer(mock_libraw, raw):
    # Quick hack because to_buffer does some ctypes acrobatics
    with mock.patch('rawkit.raw.ctypes'):
        raw.to_buffer()

    mock_libraw.libraw_dcraw_make_mem_image.assert_called_once_with(
        raw.data,
    )

    mock_libraw.libraw_dcraw_clear_mem.assert_called_once_with(
        mock_libraw.libraw_dcraw_make_mem_image(raw.data),
    )


def test_thumbnail_to_buffer(mock_libraw, raw):
    # Quick hack because thumbnail_to_buffer does some ctypes acrobatics
    with mock.patch('rawkit.raw.ctypes'):
        raw.thumbnail_to_buffer()

    mock_libraw.libraw_dcraw_make_mem_thumb.assert_called_once_with(
        raw.data,
    )

    mock_libraw.libraw_dcraw_clear_mem.assert_called_once_with(
        mock_libraw.libraw_dcraw_make_mem_thumb(raw.data),
    )


def test_metadata(mock_libraw, raw):
    metadata = raw.metadata
    assert type(metadata) is Metadata
