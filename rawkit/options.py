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

gamma_curves = namedtuple(
    'GammaCurves', ['linear', 'bt709', 'srgb', 'adobe_rgb']
)([1, 1], [1 / 2.222, 4.5], [1 / 2.4, 12.92], [256 / float(563)])
"""
Gamma curves for a few common color profiles.

  - ``linear`` --- A basic linear transfer function.
  - ``bt709`` --- The BT.709 (Rec. 709) curve used by HDTVs (uses the median
    power of sRGB, and a similar but shifted transfer function).
  - ``srgb`` --- The sRGB gamma curve (uses the max power to account for linear
    discontinuity and to attain the standard `IEC 61966-2-1` solution $K_0
    \\\\approx 0.04045 $).
  - ``adobe_rgb`` --- The correction function power for the Adobe RGB
    colorspace. The toe-slope is left off.
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

interpolation = namedtuple(
    'InterpolationAlgo', ['linear', 'vng', 'ppg', 'ahd', 'dcb', 'modified_ahd',
                          'afd', 'vcd', 'mixed_vcd_modified_ahd', 'lmmse',
                          'amaze']
)(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
"""
Constants for setting the interpolation algorithm:

    0.  Linear
    1.  VNG
    2.  PPG
    3.  AHD
    4.  DCB
    5.  Modified AHD
    6.  AFD
    7.  VCD
    8.  Mixed VCD and Modified AHD
    9.  LMMSE
    10. AMaZE

Modified AHD (5) through LMMSE (9) are only useful if you're using a version of
LibRaw with the "`LibRaw Demosaic Pack GPL2`_" built in and AMaZE (10) is only
useful if LibRaw was built with the "`LibRaw Demosaic Pack GPL3`_". If you
attepmt to use an interpolation method that's not built into your version of
LibRaw, it will silently fallback to AHD.

Usage example:

.. sourcecode:: python

    from rawkit.raw import Raw
    from rawkit.options import interpolation

    with Raw(filename="RawFile.CR2") as raw:
        raw.options.interpolation = interpolation.ahd
        raw.save("RawFile.ppm")

.. _LibRaw Demosaic Pack GPL2:
   https://github.com/LibRaw/LibRaw-demosaic-pack-GPL2
.. _LibRaw Demosaic Pack GPL3:
   https://github.com/LibRaw/LibRaw-demosaic-pack-GPL3
"""


class WhiteBalance(namedtuple('WhiteBalance',
                              ['auto', 'camera', 'greybox', 'rgbg'])):

    """
    Represents the white balance of a photo. If the camera white balance is
    used, but not present, we fallback to the other options. Other options
    white balance multipliers stack (eg. you can use auto white balance, and
    then specify a manual ``rgbg`` multiplier on top of that).

    Args:
        auto (boolean): Determines if we should automatically set the WB.
        camera (boolean): Causes us to use the camera defined WB if present.
        greybox (4 int tuple): Set the WB based on a neutral grey region of the
                               image.
        rgbg (4 float tuple): Set the WB manually based on an RGBG channel
                              multiplier.

    Returns:
        WhiteBalance: A white balance object.
    """

    __slots__ = ()

    def __new__(cls, auto=False, camera=False, greybox=None, rgbg=None):
        return super(WhiteBalance, cls).__new__(
            cls, auto, camera, greybox, rgbg)


class Options(object):

    """
    Represents a set of options which can be used when processing raw data.

    Args:
        attrs (dict): A subscriptable object from which to take the initial
                      state of the options object.
    """

    __slots__ = [
        '_bps',
        '_brightness',
        '_auto_brightness',
        '_auto_brightness_threshold',
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
        '_colorspace',
        '_output_profile',
        '_input_profile',
        '_use_camera_profile',
        '_cropbox',
        '_gamma',
        '_interpolation',
        '_auto_stretch',
        '_rotation',
        '_dark_frame',
        '_green_matching',
        '_bad_pixels_file',
        '_median_filter_passes',
        '_adjust_maximum_threshold',
    ]

    def __init__(self, attrs=None):
        """
        Create the options object, initializing values to ``None`` or their
        corresponding value from `attrs`.
        """
        for i in self.__slots__:
            try:
                param = i[1:]
                setattr(self, param, attrs[param])
            except (KeyError, TypeError):
                setattr(self, i, None)

    def __iter__(self):
        """Allow iterating over the options."""
        idx = 0
        while True:
            idx += 1
            try:
                yield self.keys()[idx - 1]
            except IndexError:
                raise StopIteration

    def __repr__(self):
        """Represents the options as a dict."""
        return repr(dict(self))

    def keys(self):
        """
        A list of keys which have a value other than ``None`` and which have
        been set by the user (even if those options are set to the default
        value).

        Returns:
            tuple: List of option keys which have been set.
        """
        return [slot[1:] for slot in self.__slots__ if getattr(self, slot) is
                not None]

    def values(self):
        """
        The values of all options which appear in :func:`keys`.

        Returns:
            tuple: List of options values.
        """
        return [self.__getitem__(k) for k in self.keys()]

    def __getitem__(self, k):
        """
        Allow accessing options with dictionary syntax eg. ::

            opts['half_size'].
        """
        return getattr(self, k)

    @option(param='output_color', ctype=ctypes.c_int)
    def colorspace(self):
        """
        Sets the colorspace used for the output image. Supported colorspaces
        are defined as constants in :class:`rawkit.options.colorspaces`.

        :type: :class:`int`
        :default: :class:`rawkit.options.colorspaces.srgb`
        :dcraw: ``-o``
        :libraw: :class:`libraw.structs.libraw_output_params_t.output_color`
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
        :libraw: :class:`libraw.structs.libraw_output_params_t.highlight`
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
        :libraw: :class:`libraw.structs.libraw_output_params_t.use_auto_wb`
                 :class:`libraw.structs.libraw_output_params_t.use_camera_wb`
                 :class:`libraw.structs.libraw_output_params_t.greybox`
                 :class:`libraw.structs.libraw_output_params_t.user_mul`
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
        Leaf, and Phase One cameras (and DNG files).

        Note that we differ from the LibRaw defaults on this option. LibRaw
        defaults to true if the photo is in DNG format or the camera white
        balance is being used, and false otherwise. rawkit always defaults to
        true.

        :type: :class:`boolean`
        :default: True
        :dcraw: ``+M``
                ``-M``
        :libraw: :class:`libraw.libraw_output_params_t.use_camera_matrix`
        """
        return True

    @option(param='shot_select', ctype=ctypes.c_uint)
    def shot(self):
        """
        Selects the shot to process for raw images that contain multiple
        images.

        :type: :class:`int`
        :default: 0
        :dcraw: ``-s``
        :libraw: :class:`libraw.structs.libraw_output_params_t.shot_select`
        """
        return None

    @option(param='user_sat', ctype=ctypes.c_int)
    def saturation(self):
        """
        Determines the saturation level of the output image.

        :type: :class:`int`
        :default: None
        :dcraw: ``-S``
        :libraw: :class:`libraw.structs.libraw_output_params_t.user_sat`
        """
        return None

    @option(param='four_color_rgb', ctype=ctypes.c_int)
    def rgbg_interpolation(self):
        """
        Determines if we should use four channel RGB interpolation.

        :type: :class:`boolean`
        :default: False
        :dcraw: ``-f``
        :libraw: :class:`libraw.structs.libraw_output_params_t.four_color_rgb`
        """
        return False

    @option(param='threshold', ctype=ctypes.c_float)
    def noise_threshold(self):
        """
        Sets the threshold for noise reduction using wavelet denoising.

        :type: :class:`float`
        :default: None
        :dcraw: ``-n``
        :libraw: :class:`libraw.structs.libraw_output_params_t.threshold`
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
        :libraw: :class:`libraw.structs.libraw_output_params_t.half_size`
        """
        return False

    @option(param='user_black', ctype=ctypes.c_int)
    def darkness(self):
        """
        Raise the black level of a photo.

        :type: :class:`int`
        :default: None
        :dcraw: ``-k``
        :libraw: :class:`libraw.structs.libraw_output_params_t.user_black`
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
        :libraw: :class:`libraw.structs.libraw_output_params_t.aber`
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
        :libraw: :class:`libraw.structs.libraw_output_params_t.output_bps`
        """
        return 8

    @bps.setter
    def bps(self, value):
        if value in (8, 16):
            self._bps = value
        else:
            raise ValueError("BPS must be 8 or 16")

    @option(param='cropbox', ctype=(ctypes.c_uint * 4))
    def cropbox(self):
        """
        Crops the image.

        :type: :class:`4 float tuple`
        :default: None
        :dcraw: None
        :libraw: :class:`libraw.structs.libraw_output_params_t.cropbox`
        """
        return None

    @option(param='gamm', ctype=(ctypes.c_double * 6))
    def gamma(self):
        """
        Sets the gamma-curve of the photo. The two values in the tuple
        correspond to:

            - gamma[0] --- Correction function power (inverted Gamma power,
              $\\\\gamma^{-1}$)
            - gamma[1] --- toe-slope ($\\\\phi$)

        For a simple power curve, set the toe-slope to zero.

        :type: :class:`2 double tuple`
        :default: None
        :dcraw: ``-g``
        :libraw: :class:`libraw.structs.libraw_output_params_t.gamm`
        """
        return None

    @option(param='interpolation', ctype=ctypes.c_uint)
    def interpolation(self):
        """
        Sets the interpolation algorithm.

        :type: :class:`rawkit.options.interpolation`
        :default: `ahd`
        :dcraw: ``-q``
        :libraw: :class:`libraw.structs.libraw_output_params_t.user_qual`
        """
        return interpolation.ahd

    @option(param='bright', ctype=ctypes.c_float)
    def brightness(self):
        """
        Sets the brightness level by dividing the white level by this value.
        This is ignored if :class:`~auto_brightness` is ``True``.

        :type: :class:`float`
        :default: 1.0
        :dcraw: ``-b``
        :libraw: :class:`libraw.structs.libraw_output_params_t.bright`
        """
        return None

    @option(param='auto_bright_thr', ctype=ctypes.c_float)
    def auto_brightness_threshold(self):
        """
        The allowable percentage of clipped pixels when
        :class:`~auto_brightness` is used.

        :type: :class:`float`
        :default: 0.001 (0.1%)
        :dcraw: None
        :libraw: :class:`libraw.structs.libraw_output_params_t.auto_bright_thr`
        """
        return 0.001

    @option
    def auto_brightness(self):
        """
        Set the brightness automatically based on the image histogram and the
        :class:`~auto_brightness_threshold`.

        :type: :class:`boolean`
        :default: True
        :dcraw: ``-W``
        :libraw: :class:`libraw.structs.libraw_output_params_t.no_auto_bright`
        """
        return True

    @auto_brightness.param_writer
    def auto_brightness(self, param):
        param.no_auto_bright = ctypes.c_int(not self.auto_brightness)

    @option(param='use_fuji_rotate', ctype=ctypes.c_int)
    def auto_stretch(self):
        """
        Stretches images taken on cameras with non-square pixels to the correct
        aspect ratio. For Fuji Super CCD cameras, rotates the image 45 degrees.
        This guarantees that the output pixels share a 1:1 correspondence with
        the raw pixels.

        :type: :class:`boolean`
        :default: True
        :dcraw: ``-j``
        :libraw: :class:`libraw.structs.libraw_output_params_t.use_fuji_rotate`
        """
        return True

    @option
    def rotation(self):
        """
        Rotates the image by the given number of degrees. Must be a multiple of
        90 (0, 90, 180, 270, etc).

        The default (None) is to use the rotation provided by the camera.

        :type: :class:`int`
        :default: None
        :dcraw: ``-t``
        :libraw: :class:`libraw.structs.libraw_output_params_t.user_flip`
        """
        return None

    @rotation.setter
    def rotation(self, value):
        if value is not None and value > 0:
            value = ((value + 3600) % 360)

        if value in (None, 0, 90, 180, 270):
            self._rotation = value
        else:
            raise ValueError('Rotation must be None (use camera rotation) or '
                             'a multiple of 90')

    @rotation.param_writer
    def rotation(self, params):
        params.user_flip = ctypes.c_int({
            270: 5,
            180: 3,
            90: 6,
            0: 0
        }[self.rotation])

    @option
    def dark_frame(self):
        """
        A dark frame in 16-bit PGM format. This may either be a path to an
        existing file, or an instance of :class:`rawkit.raw.DarkFrame`.

        :type: :class:`rawkit.raw.DarkFrame`
               :class:`str`
        :default: None
        :dcraw: ``-K``
        :libraw: :class:`libraw.structs.libraw_output_params_t.dark_frame`
        """
        return None

    @dark_frame.setter
    def dark_frame(self, value):
        self._dark_frame = value

    @dark_frame.param_writer
    def dark_frame(self, params):
        try:
            self.dark_frame.save()
            params.dark_frame = ctypes.c_char_p(
                self.dark_frame.name.encode('utf-8')
            )
        except AttributeError:
            params.dark_frame = ctypes.c_char_p(
                self.dark_frame.encode('utf-8')
            )

    @option(param='green_matching', ctype=ctypes.c_int)
    def green_matching(self):
        """
        Performs a second post-processing pass to correct for green channel
        imbalance.

        :type: :class:`boolean`
        :default: False
        :dcraw: None
        :libraw: :class:`libraw.structs.libraw_output_params_t.green_matching`
        """
        return False

    @option(param='output_profile', ctype=ctypes.c_char_p)
    def output_profile(self):
        """
        Path to an ICC color profile file containing the output profile. Only
        used if the version of LibRaw that you're linking against was compiled
        with LCMS support.

        :type: :class:`string`
        :default: None
        :dcraw: ``-o``
                ``-p``
        :libraw: :class:`libraw.structs.libraw_output_params_t.output_profile`
        """
        return None

    @option(param='camera_profile', ctype=ctypes.c_char_p)
    def input_profile(self):
        """
        Path to an ICC color profile file containing the input profile. Only
        used if the version of LibRaw that you're linking against was compiled
        with LCMS support.

        Note that LibRaw defines a magic string, 'embed', which causes it to
        use the profile embedded in the raw image if present. This is the same
        as setting the :class:`~use_camera_profile` option.

        :type: :class:`string`
        :default: None
        :dcraw: ``-o``
                ``-p``
        :libraw: :class:`libraw.structs.libraw_output_params_t.camera_profile`
        """
        return None

    @option
    def use_camera_profile(self):
        """
        True if we should use the embedded camera profile (if present in the
        raw file and we're linking against a version of LibRaw with LCMS
        support).

        :type: :class:`boolean`
        :default: True
        :dcraw: ``-o``
                ``-p``
        :libraw: :class:`libraw.structs.libraw_output_params_t.camera_profile`
        """
        return True

    @use_camera_profile.setter
    def use_camera_profile(self, value):
        self._use_camera_profile = value

    @use_camera_profile.param_writer
    def use_camera_profile(self, params):
        if self.use_camera_profile:
            params.camera_profile = ctypes.c_char_p(b'embed')
        else:
            params.camera_profile = None

    @option(param='bad_pixels', ctype=ctypes.c_char_p)
    def bad_pixels_file(self):
        """
        Points to a bad pixels map in dcraw format: ::

            column row unix-timestamp\\n

        :type: :class:`str`
        :default: None
        :dcraw: ``-P``
        :libraw: :class:`libraw.structs.libraw_output_params_t.bad_pixels`
        """
        return None

    @option(param='med_passes', ctype=ctypes.c_int)
    def median_filter_passes(self):
        """
        Useful for cleaning up color artifacts by running a 3x3 median filter
        over the R-G and B-G channels.

        :type: :class:`int`
        :default: 0
        :dcraw: ``-m``
        :libraw: :class:`libraw.structs.libraw_output_params_t.med_passes`
        """
        return 0

    @option(param='adjust_maximum_thr', ctype=ctypes.c_float)
    def adjust_maximum_threshold(self):
        """
        Automatically adjusts the maximum pixel value based on per channel
        maximum data.

        Note:

            If this value is set above 0.99999, the default value will be used
            instead. If it is set below 0.00001, no adjustment will happen.

        :type: :class:`float`
        :default: 0.75
        :dcraw: None
        :libraw:
            :class:`libraw.structs.libraw_output_params_t.adjust_maximum_thr`
        """
        return 0

    def _map_to_libraw_params(self, params):
        """
        Internal method that writes rawkit options into the libraw options
        struct with the proper C data types.

        Args:
            params (libraw.structs.libraw_output_params_t):
                The output params struct to set.
        """
        for slot in self.__slots__:
            prop = slot[1:]
            opt = getattr(Options, prop)
            if type(opt) is option and getattr(self, prop) is not None:
                opt.write_param(self, params)

        # This generally isn't needed, except for testing.
        return params
