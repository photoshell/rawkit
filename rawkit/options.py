""":mod:`rawkit.options` --- High level options for processing raw files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import ctypes

from collections import namedtuple


class option(object):

    """
    The :class:`option` decorator is an internal decorator which allows you to
    define an option in a clean manner (specifying its name and how it maps to
    the libraw params).
    """

    def __init__(self, param=None, ctype=None):
        if callable(param):
            func = param
            param = None
        else:
            func = None
        self._prepare_func(func)
        self.param = param
        self.ctype = ctype
        self.setter_func = None
        self.param_func = None

    def _prepare_func(self, func):
        self.func = func
        if func is not None:
            self.__doc__ = getattr(func, '__doc__')
            self.__name__ = getattr(func, '__name__')
            self.internal_name = '_{name}'.format(name=self.__name__)
            self.__module__ = getattr(func, '__module__')

    def __call__(self, func=None):
        self._prepare_func(func)
        if func is None:
            raise TypeError("option should not be called except as a property")
        self.func = func
        return self

    def setter(self, func):
        self.setter_func = func
        return self

    def param_writer(self, func):
        self.param_func = func
        return self

    def write_param(self, obj, params):
        if self.param_func is None:
            val = self.__get__(obj, None)
            try:
                setattr(params, self.param, self.ctype(*val))
            except TypeError:
                setattr(params, self.param, self.ctype(val))
        else:
            self.param_func(obj, params)

    def __set__(self, obj, value):
        if self.setter_func is None:
            setattr(obj, self.internal_name, value)
        else:
            self.setter_func(obj, value)

    def __get__(self, obj, cls):
        try:
            val = getattr(obj, self.internal_name)
            if val is None:
                return self.func(obj)
            else:
                return val
        except AttributeError:
            # We're probably generating the documentation...
            return self

highlight_modes = namedtuple(
    'HighlightMode', ['clip', 'ignore', 'blend', 'reconstruct']
)(0, 1, 2, 5)
"""
Constants for setting the highlight mode.

  - ``clip`` --- Clip all highlights to white (default).
  - ``ignore`` --- Leave highlights unclipped.
  - ``blend`` --- Blend clipped and unclipped highlights.
  - ``reconstruct`` --- A good average value for reconstruction of clipped
    highlights which compromises between favoring whites and favoring colors.
"""

colorspaces = namedtuple(
    'ColorSpaces', ['raw', 'srgb', 'adobe_rgb', 'wide_gammut_rgb',
                    'kodak_prophoto_rgb', 'xyz']
)(0, 1, 2, 3, 4, 5)
"""
Constants for setting the colorspace.

  - ``raw_color`` --- Raw colorspace (unique to each camera)
  - ``srgb`` --- sRGB D65 (default colorspace)
  - ``adobe_rgb`` --- Adobe RGB (1998) D65
  - ``wide_gammut_rgb`` ---  Wide Gamut RGB D65
  - ``kodak_prophoto_rgb`` --- Kodak ProPhoto RGB D65
  - ``xyz`` --- XYZ colorspace
"""


class WhiteBalance(namedtuple('WhiteBalance',
                              ['auto', 'camera', 'greybox', 'rgbg'])):

    """
    Represents the white balance of a photo. If the camera white balance is
    used, but not present, we fallback to the other options. Other options
    white balance multipliers stack (eg. you can use auto white balance, and
    then specify a manual ``rgbg`` multiplier on top of that).

    :param auto: determines if we should automatically set the WB
    :type auto: :class:`boolean`
    :param camera: causes us to use the camera defined WB if present
    :type camera: :class:`boolean`
    :param greybox: set the WB based on a neutral grey region of the image
    :type greybox: :class:`4 int tuple`
    :param rgbg: set the WB manually based on an RGBG channel multiplier
    :type rgbg: :class:`4 float tuple`
    :returns: A white blance object
    :rtype: :class:`WhiteBalance`
    """

    __slots__ = ()

    def __new__(cls, auto=False, camera=False, greybox=None, rgbg=None):
        return super(WhiteBalance, cls).__new__(
            cls, auto, camera, greybox, rgbg)


class Options(object):

    """
    Represents a set of options which can be used when processing raw data.
    """

    __slots__ = [
        '_bps',
        '_brightness',
        '_chromatic_aberration',
        '_darkness',
        '_half_size',
        '_noise_threshold',
        '_rgbg_interpolation',
        '_saturation',
        '_shot',
        '_use_camera_matrix',
        '_white_balance',
        '_highlight_mode',
        '_colorspace'
    ]
    """The options which are supported by this class."""

    def __init__(self):
        """
        Create the options object, initializing values to ``None``.
        """
        for i in self.__slots__:
            setattr(self, i, None)

    @option(param='output_color', ctype=ctypes.c_int)
    def colorspace(self):
        """
        Sets the colorspace used for the output image. Supported colorspaces
        are defined as constants in :class:`rawkit.options.colorspaces`.

        :type: :class:`int`
        :default: :class:`rawkit.options.colorspaces.srgb`
        :dcraw: ``-o``
        :libraw: :class:`rawkit.libraw.libraw_output_params_t.output_color`
        """
        return colorspaces.srgb

    @option(param='highlight', ctype=ctypes.c_int)
    def highlight_mode(self):
        """
        The mode for dealing with highlights in the image. Some constants have
        been defined in :class:`rawkit.options.highlight_modes` to make things
        easier, or you can set an integer directly.

        Integers that are greater than or equal to 3 will attempt to
        reconstruct highlights. Lower numbers favor whites, and higher colors
        favor colors. :class:`rawkit.options.RECONSTRUCT` (5) is a good
        compromise.

        :type: :class:`int`
        :default: :class:`rawkit.options.highlight_modes.clip`
        :dcraw: ``-H``
        :libraw: :class:`rawkit.libraw.libraw_output_params_t.highlight`
        """
        return highlight_modes.clip

    @option
    def white_balance(self):
        """
        The white balance of the image.

        :type: :class:`rawkit.options.WhiteBalance`
        :default: WhiteBalance(auto=True, camera=True)
        :dcraw: ``-a``
                ``-w``
                ``-A``
                ``-r``
        :libraw: :class:`rawkit.libraw.libraw_output_params_t.use_auto_wb`
                 :class:`rawkit.libraw.libraw_output_params_t.use_camera_wb`
                 :class:`rawkit.libraw.libraw_output_params_t.greybox`
                 :class:`rawkit.libraw.libraw_output_params_t.user_mul`
        """
        return WhiteBalance(auto=True, camera=True)

    @white_balance.param_writer
    def white_balance(self, params):
        if self.white_balance.greybox is not None:
            params.greybox = (ctypes.c_uint * 4)(*self.white_balance.greybox)
        if self.white_balance.rgbg is not None:
            params.user_mul = (ctypes.c_float * 4)(*self.white_balance.rgbg)
        params.use_camera_wb = ctypes.c_int(self.white_balance.camera)
        params.use_auto_wb = ctypes.c_int(self.white_balance.auto)

    @option(param='use_camera_matrix', ctype=ctypes.c_int)
    def use_camera_matrix(self):
        """
        Use the color matrix from the raw's metadata. Only affects Olympus,
        Leaf, and Phase One cameras (and DNG files). Default is True if the
        photo is in DNG format or the camera white balance is being used, False
        otherwise.

        :type: :class:`boolean`
        :default: 0
        :dcraw: ``+M``
                ``-M``
        :libraw: :class:`libraw.libraw_output_params_t.use_camera_matrix`
        """
        return None

    @option(param='shot_select', ctype=ctypes.c_uint)
    def shot(self):
        """
        Selects the shot to process for raw images that contain multiple
        images.

        :type: :class:`int`
        :default: 0
        :dcraw: ``-s``
        :libraw: :class:`rawkit.libraw.libraw_output_params_t.shot_select`
        """
        return None

    @option(param='user_sat', ctype=ctypes.c_int)
    def saturation(self):
        """
        Determines the saturation level of the output image.

        :type: :class:`int`
        :default: None
        :dcraw: ``-S``
        :libraw: :class:`rawkit.libraw.libraw_output_params_t.user_sat`
        """
        return None

    @option(param='four_color_rgb', ctype=ctypes.c_int)
    def rgbg_interpolation(self):
        """
        Determines if we should use four channel RGB interpolation.

        :type: :class:`boolean`
        :default: False
        :dcraw: ``-f``
        :libraw: :class:`rawkit.libraw.libraw_output_params_t.four_color_rgb`
        """
        return False

    @option(param='threshold', ctype=ctypes.c_float)
    def noise_threshold(self):
        """
        Sets the threshold for noise reduction using wavelet denoising.

        :type: :class:`float`
        :default: None
        :dcraw: ``-n``
        :libraw: :class:`rawkit.libraw.libraw_output_params_t.threshold`
        """
        return None

    @option(param='half_size', ctype=ctypes.c_int)
    def half_size(self):
        """
        When developing the image, output it at 50% size. This makes developing
        preview images much faster.

        :type: :class:`boolean`
        :default: False
        :dcraw: ``-h``
        :libraw: :class:`rawkit.libraw.libraw_output_params_t.half_size`
        """
        return False

    @option(param='user_black', ctype=ctypes.c_int)
    def darkness(self):
        """
        Raise the black level of a photo.

        :type: :class:`int`
        :default: None
        :dcraw: ``-k``
        :libraw: :class:`rawkit.libraw.libraw_output_params_t.user_black`
        """
        return None

    @option
    def chromatic_aberration(self):
        """
        A Red-Blue scale factor that's used to correct for chromatic aberration
        by scaling the respective channels.

        eg. ::

            # (red_scale, blue_scale)
            raw.options.chromatic_aberration = (0.999, 1.001)

        :type: :class:`double tuple`
        :default: (1, 1)
        :dcraw: ``-C``
        :libraw: :class:`rawkit.libraw.libraw_output_params_t.aber`
        """
        return (1, 1)

    @chromatic_aberration.param_writer
    def chromatic_aberration(self, params):
        params.aber = (ctypes.c_double * 4)(*(
            self.chromatic_aberration[0],
            0,  # TODO: What is this index used for?
            self.chromatic_aberration[1],
            0  # TODO: What is this index used for?
        ))

    @option(param='output_bps', ctype=ctypes.c_int)
    def bps(self):
        """
        Set the bits per sample used for the photo (8 or 16).
        Setting this to 16 is effectively the same as running dcraw with the
        ``-4`` option.

        :type: :class:`int`
        :default: 8
        :dcraw: ``-4``
        :libraw: :class:`rawkit.libraw.libraw_output_params_t.output_bps`
        """
        return 8

    @bps.setter
    def bps(self, value):
        if value in (8, 16):
            self._bps = value
        else:
            raise ValueError("BPS must be 8 or 16")

    @option(param='bright', ctype=ctypes.c_float)
    def brightness(self):
        """
        The brightness of the image.

        :type: :class:`float`
        :default: 1.0
        :dcraw: ``-b``
        :libraw: :class:`rawkit.libraw.libraw_output_params_t.bright`
        """
        return 1.0

    def _map_to_libraw_params(self, params):
        """
        Internal method that writes rawkit options into the libraw options
        struct with the proper C data types.

        :param params: the output params struct to set
        :type params: :class:`rawkit.libraw.libraw_output_params_t`
        """
        for slot in self.__slots__:
            prop = slot[1:]
            opt = getattr(Options, prop)
            if type(opt) is option and getattr(self, prop) is not None:
                opt.write_param(self, params)
