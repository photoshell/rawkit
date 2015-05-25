import pytest

from mock import Mock
from rawkit.options import option, Options, WhiteBalance

# @option decorator tests


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
    params = Mock()
    options.white_balance = WhiteBalance(greybox=(0, 0, 0, 0),
                                         rgbg=(0, 0, 0, 0))
    options._map_to_libraw_params(params)
    assert params.greybox is not None
    assert params.rgbg is not None


def test_bps_must_be_8_or_16(options):
    with pytest.raises(ValueError):
        options.bps = 5


def test_map_params_fails_on_invalid(options):
    # with pytest.raises(AttributeError):
    params = Mock()
    options._map_to_libraw_params(params)
