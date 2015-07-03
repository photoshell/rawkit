import pytest

from mock import Mock
from rawkit.options import option, Options, WhiteBalance


@pytest.fixture
def options():
    return Options()


@pytest.fixture
def opt_method():
    @option()
    def method():
        raise NotImplementedError

    return method


def test_calling_an_option_method_directly_should_error(opt_method):
    with pytest.raises(TypeError):
        opt_method()


def test_setting_a_value(options):
    # TODO: It would probably be better for these to operate on a Mock and
    # check if __set__ was called.

    # Uses normal set
    options.darkness = 1
    assert options.darkness is 1

    # Uses a special setter
    options.bps = 16
    assert options.bps == 16


def test_option_from_class_should_return_decorator():
    assert type(Options.bps) is option


def test_custom_wb_param_writer_writes_rgbg_and_greybox(options):
    options.white_balance = WhiteBalance(greybox=(7, 7, 7, 7),
                                         rgbg=(42, 42, 42, 42))
    params = options._map_to_libraw_params(Mock())

    for v in params.greybox:
        assert v == 7
    for v in params.user_mul:
        assert v == 42


def test_bps_must_be_8_or_16(options):
    with pytest.raises(ValueError):
        options.bps = 5


def test_options_are_iterable(options):
    options.half_size = True
    assert 'half_size' in options
    assert 'bps' not in options


def test_options_repr(options):
    options.half_size = True

    assert repr(options) == repr({'half_size': True})


def test_options_keys(options):
    options.half_size = True

    assert options.keys() == ['half_size']


def test_options_values(options):
    options.half_size = True

    assert options.values() == [True]


def test_set_rotation_invalid_type(options):
    with pytest.raises(TypeError):
        options.rotation = 'fish'


def test_set_rotation_value_is_reduced(options):
    options.rotation = 270 + 90
    assert options.rotation == 0

    options.rotation = 270 + 180
    assert options.rotation == 90

    options.rotation = None
    assert options.rotation is None


def test_set_rotation_invalid_value(options):
    with pytest.raises(ValueError):
        options.rotation = 93.5


def test_rotation_param_writer_values(options):
    values = {
        270: 5,
        180: 3,
        90: 6,
        0: 0
    }
    for value in values.keys():
        options.rotation = value
        params = options._map_to_libraw_params(Mock())
        assert params.user_flip.value == values[value]


def test_dark_frame_setter(options):
    options.dark_frame = 'Some String'
    assert options._dark_frame == 'Some String'


def test_dark_frame_writer(options):
    options.dark_frame = 'Some String'
    params = options._map_to_libraw_params(Mock())
    assert params.dark_frame.value == b'Some String'

    df = Mock()
    df._tmp = 'fakefile'
    df.name = df._tmp
    options.dark_frame = df
    params = options._map_to_libraw_params(Mock())
    assert params.dark_frame.value == b'fakefile'


def test_use_camera_profile_setter(options):
    options.use_camera_profile = False
    assert options.use_camera_profile is False

    options.use_camera_profile = True
    assert options.use_camera_profile is True


def test_use_camera_profile_writer(options):
    options.use_camera_profile = True
    params = options._map_to_libraw_params(Mock())
    assert params.camera_profile.value == b'embed'

    options.use_camera_profile = False
    params = options._map_to_libraw_params(Mock())
    assert params.camera_profile is None
