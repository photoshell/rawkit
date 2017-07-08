""":mod:`libraw.structs` --- LibRaw struct definitions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from ctypes import *  # noqa


class ph1_t(Structure):

    """Contains color data read by Phase One cameras."""
    _fields_ = [
        ('format', c_int),
        ('key_off', c_int),
        ('tag_21a', c_int),
        ('t_black', c_int),
        ('split_col', c_int),
        ('black_col', c_int),
        ('split_row', c_int),
        ('black_row', c_int),
        ('tag_210', c_float),
    ]


class libraw_iparams_t(Structure):

    """The primary parameters of the image."""
    _fields_ = [
        ('guard', c_char * 4),
        ('make', c_char * 64),
        ('model', c_char * 64),
        ('software', c_char * 64),
        ('raw_count', c_uint),
        ('dng_version', c_uint),
        ('is_foveon', c_uint),
        ('colors', c_int),
        ('filters', c_uint),
        ('xtrans', c_char * 6 * 6),
        ('xtrans_abs', c_char * 6 * 6),
        ('cdesc', c_char * 5),
        ('xmplen', c_uint),
        ('xmpdata', POINTER(c_char)),
    ]


class libraw_image_sizes_t(Structure):

    """Describes the size of the image."""
    _fields_ = [
        ('raw_height', c_ushort),
        ('raw_width', c_ushort),
        ('height', c_ushort),
        ('width', c_ushort),
        ('top_margin', c_ushort),
        ('left_margin', c_ushort),
        ('iheight', c_ushort),
        ('iwidth', c_ushort),
        ('raw_pitch', c_uint),
        ('pixel_aspect', c_double),
        ('flip', c_int),
        ('mask', c_int * 8 * 4),
    ]


class libraw_dng_color_t(Structure):

    _fields_ = [
        ('illuminant', c_ushort),
        ('calibration', c_float * 4 * 4),
        ('colormatrix', c_float * 4 * 3),
        ('forwardmatrix', c_float * 3 * 4),
    ]


class libraw_canon_makernotes_t(Structure):

    _fields_ = [
        ('CanonColorDataVer', c_int),
        ('CanonColorDataSubVer', c_int),
        ('SpecularWhiteLevel', c_int),
        ('ChannelBlackLevel', c_int * 4),
        ('AverageBlackLevel', c_int),
        ('MeteringMode', c_short),
        ('SpotMeteringMode', c_short),
        ('FlashMeteringMode', c_char),
        ('FlashExposureLock', c_short),
        ('ExposureMode', c_short),
        ('AESetting', c_short),
        ('HighlightTonePriority', c_char),
        ('ImageStabilization', c_short),
        ('FocusMode', c_short),
        ('AFPoint', c_short),
        ('FocusContinuous', c_short),
        ('AFPointsInFocus30D', c_short),
        ('AFPointsInFocus1D', c_char * 8),
        ('AFPointsInFocus5D', c_ushort),
        ('AFAreaMode', c_ushort),
        ('NumAFPoints', c_ushort),
        ('ValidAFPoints', c_ushort),
        ('AFImageWidth', c_ushort),
        ('AFImageHeight', c_ushort),
        ('AFAreaWidths', c_short * 61),
        ('AFAreaHeights', c_short * 61),
        ('AFAreaXPositions', c_short * 61),
        ('AFAreaYPositions', c_short * 61),
        ('AFPointsInFocus', c_short * 4),
        ('AFPointsSelected', c_short * 4),
        ('PrimaryAFPoint', c_ushort),
        ('FlashMode', c_short),
        ('FlashActivity', c_short),
        ('FlashBits', c_short),
        ('ManualFlashOutput', c_short),
        ('FlashOutput', c_short),
        ('FlashGuideNumber', c_short),
        ('ContinuousDrive', c_short),
        ('SensorWidth', c_short),
        ('SensorHeight', c_short),
        ('SensorLeftBorder', c_short),
        ('SensorTopBorder', c_short),
        ('SensorRightBorder', c_short),
        ('SensorBottomBorder', c_short),
        ('BlackMaskLeftBorder', c_short),
        ('BlackMaskTopBorder', c_short),
        ('BlackMaskRightBorder', c_short),
        ('BlackMaskBottomBorder', c_short),
    ]


class libraw_dng_levels_t(Structure):

    _fields_ = [
        ('dng_cblack', c_uint * 4102),
        ('dng_black', c_uint),
        ('dng_whitelevel', c_uint * 4),
        ('dng_blacklevel', c_float * 4),
        ('analogbalance', c_float * 4),
    ]


class libraw_P1_color_t(Structure):

    _fields_ = [
        ('romm_cam', c_float * 9),
    ]


class libraw_colordata_t(Structure):

    """Describes all color data of the image."""
    _fields_ = [
        ('curve', c_ushort * 0x10000),
        ('cblack', c_uint * 4102),
        ('black', c_uint),
        ('data_maximum', c_uint),
        ('maximum', c_uint),
        ('linear_max', c_long * 4),
        ('fmaximum', c_float),
        ('fnorm', c_float),
        ('white', c_ushort * 8 * 8),
        ('cam_mul', c_float * 4),
        ('pre_mul', c_float * 4),
        ('cmatrix', c_float * 3 * 4),
        ('ccm', c_float * 3 * 4),
        ('rgb_cam', c_float * 3 * 4),
        ('cam_xyz', c_float * 4 * 3),
        ('phase_one_data', ph1_t),
        ('flash_used', c_float),
        ('canon_ev', c_float),
        ('model2', c_char * 64),
        ('UniqueCameraModel', c_char * 64),
        ('LocalizedCameraModel', c_char * 64),
        ('profile', c_void_p),
        ('profile_length', c_uint),
        ('black_stat', c_uint * 8),
        ('dng_color', libraw_dng_color_t * 2),
        ('dng_levels', libraw_dng_levels_t),
        ('baseline_exposure', c_float),
        ('WB_Coeffs', c_int * 256 * 4),
        ('WBCT_Coeffs', c_float * 64 * 5),
        ('P1_color', libraw_P1_color_t * 2),
    ]


class libraw_gps_info_t(Structure):

    """GPS data for the image."""
    _fields_ = [
        ('latitude', c_float * 3),
        ('longitude', c_float * 3),
        ('gpstimestamp', c_float * 3),
        ('altitude', c_float),
        ('altref', c_char),
        ('latref', c_char),
        ('longref', c_char),
        ('gpsstatus', c_char),
        ('gpsparsed', c_char),
    ]


class libraw_imgother_t(Structure):

    """
    Information read from the raw file that is unnecessary for raw processing.
    """
    _fields_ = [
        ('iso_speed', c_float),
        ('shutter', c_float),
        ('aperture', c_float),
        ('focal_len', c_float),
        ('timestamp', c_uint),  # time_t
        ('shot_order', c_uint),
        ('gpsdata', c_uint * 32),
        ('parsed_gps', libraw_gps_info_t),
        ('desc', c_char * 512),
        ('artist', c_char * 64),
        ('FlashEC', c_float),
    ]


class libraw_thumbnail_t(Structure):

    """Describes the thumbnail image embedded in the raw file."""
    _fields_ = [
        ('tformat', c_uint),  # LibRaw_thumbnail_formats
        ('twidth', c_ushort),
        ('theight', c_ushort),
        ('tlength', c_uint),
        ('tcolors', c_int),
        ('thumb', POINTER(c_char)),
    ]


class libraw_internal_output_params_t(Structure):

    _fields_ = [
        ('mix_green', c_uint),
        ('raw_color', c_uint),
        ('zero_is_bad', c_uint),
        ('shrink', c_ushort),
        ('fuji_width', c_ushort),
    ]


class libraw_rawdata_t(Structure):

    """
    Raw image data (after it has been unpacked) and a backup copy of color info
    used during post processing.
    """
    _fields_ = [
        ('raw_alloc', c_void_p),
        ('raw_image', POINTER(c_ushort)),
        ('color4_image', POINTER(c_ushort * 4)),
        ('color3_image', POINTER(c_ushort * 3)),
        ('float_image', POINTER(c_float)),
        ('float3_image', POINTER(c_float * 3)),
        ('float4_image', POINTER(c_float * 4)),
        ('ph1_cblack', POINTER(c_short * 2)),
        ('ph1_rblack', POINTER(c_short * 2)),
        ('iparams', libraw_iparams_t),
        ('sizes', libraw_image_sizes_t),
        ('ioparams', libraw_internal_output_params_t),
        ('color', libraw_colordata_t),
    ]


class libraw_output_params_t(Structure):

    """Output parameters for processing the image with dcraw."""
    _fields_ = [
        ('greybox', c_uint * 4),
        ('cropbox', c_uint * 4),
        ('aber', c_double * 4),
        ('gamm', c_double * 6),
        ('user_mul', c_float * 4),
        ('shot_select', c_uint),
        ('bright', c_float),
        ('threshold', c_float),
        ('half_size', c_int),
        ('four_color_rgb', c_int),
        ('highlight', c_int),
        ('use_auto_wb', c_int),
        ('use_camera_wb', c_int),
        ('use_camera_matrix', c_int),
        ('output_color', c_int),
        ('output_profile', c_char_p),
        ('camera_profile', c_char_p),
        ('bad_pixels', c_char_p),
        ('dark_frame', c_char_p),
        ('output_bps', c_int),
        ('output_tiff', c_int),
        ('user_flip', c_int),
        ('user_qual', c_int),
        ('user_black', c_int),
        ('user_cblack', c_int * 4),
        ('user_sat', c_int),
        ('med_passes', c_int),
        ('auto_bright_thr', c_float),
        ('adjust_maximum_thr', c_float),
        ('no_auto_bright', c_int),
        ('use_fuji_rotate', c_int),
        ('green_matching', c_int),
        ('dcb_iterations', c_int),
        ('dcb_enhance_fl', c_int),
        ('fbdd_noiserd', c_int),
        ('eeci_refine', c_int),
        ('es_med_passes', c_int),
        ('ca_correc', c_int),
        ('cared', c_float),
        ('cablue', c_float),
        ('cfaline', c_int),
        ('linenoise', c_float),
        ('cfa_clean', c_int),
        ('lclean', c_float),
        ('cclean', c_float),
        ('cfa_green', c_int),
        ('green_thresh', c_float),
        ('exp_correc', c_int),
        ('exp_shift', c_float),
        ('exp_preser', c_float),
        ('wf_debanding', c_int),
        ('wf_deband_treshold', c_float * 4),
        ('use_rawspeed', c_int),
        ('use_dngsdk', c_int),
        ('no_auto_scale', c_int),
        ('no_interpolation', c_int),
        ('raw_processing_options', c_uint),
        ('sony_arw2_posterization_thr', c_int),
        ('coolscan_nef_gamma', c_float),
        ('p4shot_order', c_char * 5),
        ('custom_camera_strings', POINTER(c_char_p)),
    ]


class libraw_nikonlens_t(Structure):

    _fields_ = [
        ('NikonEffectiveMaxAp', c_float),
        ('NikonLensIDNumber', c_ubyte),
        ('NikonLensFStops', c_ubyte),
        ('NikonMCUVersion', c_ubyte),
        ('NikonLensType', c_ubyte),
    ]


class libraw_dnglens_t(Structure):

    _fields_ = [
        ('MinFocal', c_float),
        ('MaxFocal', c_float),
        ('MaxAp4MinFocal', c_float),
        ('MaxAp4MaxFocal', c_float),
    ]


class libraw_makernotes_lens_t(Structure):

    _fields_ = [
        ('LensID', c_ulonglong),
        ('Lens', c_char * 128),
        ('LensFormat', c_ushort),
        ('LensMount', c_ushort),
        ('CamID', c_ulonglong),
        ('CameraFormat', c_ushort),
        ('CameraMount', c_ushort),
        ('body', c_char * 64),
        ('FocalType', c_short),
        ('LensFeatures_pre', c_char * 16),
        ('LensFeatures_suf', c_char * 16),
        ('MinFocal', c_float),
        ('MaxFocal', c_float),
        ('MaxAp4MinFocal', c_float),
        ('MaxAp4MaxFocal', c_float),
        ('MinAp4MinFocal', c_float),
        ('MinAp4MaxFocal', c_float),
        ('MaxAp', c_float),
        ('MinAp', c_float),
        ('CurFocal', c_float),
        ('CurAp', c_float),
        ('MaxAp4CurFocal', c_float),
        ('MinAp4CurFocal', c_float),
        ('MinFocusDistance', c_float),
        ('FocusRangeIndex', c_float),
        ('LensFStops', c_float),
        ('TeleconverterID', c_ulonglong),
        ('Teleconverter', c_char * 128),
        ('AdapterID', c_ulonglong),
        ('Adapter', c_char * 128),
        ('AttachmentID', c_ulonglong),
        ('Attachment', c_char * 128),
        ('CanonFocalUnits', c_short),
        ('FocalLengthIn35mmFormat', c_float),
    ]


class libraw_lensinfo_t(Structure):

    _fields_ = [
        ('MinFocal', c_float),
        ('MaxFocal', c_float),
        ('MaxAp4MinFocal', c_float),
        ('MaxAp4MaxFocal', c_float),
        ('EXIF_MaxAp', c_float),
        ('LensMake', c_char * 128),
        ('Lens', c_char * 128),
        ('LensSerial', c_char * 128),
        ('InternalLensSerial', c_char * 128),
        ('FocalLengthIn35mmFormat', c_ushort),
        ('nikon', libraw_nikonlens_t),
        ('dng', libraw_dnglens_t),
        ('makernotes', libraw_makernotes_lens_t),
    ]

class libraw_processed_image_t(Structure):

    """A container for processed image data."""
    _fields_ = [
        ('type', c_uint),
        ('height', c_ushort),
        ('width', c_ushort),
        ('colors', c_ushort),
        ('bits', c_ushort),
        ('data_size', c_uint),
        ('data', c_ubyte * 1),
    ]


class libraw_decoder_info_t(Structure):

    """Describes a raw format decoder name and format."""
    _fields_ = [
        ('decoder_name', c_char_p),
        ('decoder_flags', c_uint),
    ]


class libraw_fuji_info_t(Structure):

    _fields_ = [
        ('FujiExpoMidPointShift', c_float),
        ('FujiDynamicRange', c_ushort),
        ('FujiFilmMode', c_ushort),
        ('FujiDynamicRangeSetting', c_ushort),
        ('FujiDevelopmentDynamicRange', c_ushort),
        ('FujiAutoDynamicRange', c_ushort),
        ('FocusMode', c_ushort),
        ('AFMode', c_ushort),
        ('FocusPixel', c_ushort * 2),
        ('ImageStabilization', c_ushort * 3),
        ('FlashMode', c_ushort),
        ('WB_Preset', c_ushort),
        ('ShutterType', c_ushort),
        ('ExrMode', c_ushort),
        ('Macro', c_ushort),
        ('Rating', c_uint),
        ('FrameRate', c_ushort),
        ('FrameWidth', c_ushort),
        ('FrameHeight', c_ushort),
    ]


class libraw_nikon_makernotes_t(Structure):

    _fields_ = [
        ('ExposureBracketValue', c_double),
        ('ActiveDLighting', c_ushort),
        ('ShootingMode', c_ushort),
        ('ImageStabilization', c_ubyte * 7),
        ('VibrationReduction', c_ubyte),
        ('VRMode', c_ubyte),
        ('FocusMode', c_char * 7),
        ('AFPoint', c_ubyte),
        ('AFPointsInFocus', c_ushort),
        ('ContrastDetectAF', c_ubyte),
        ('AFAreaMode', c_ubyte),
        ('PhaseDetectAF', c_ubyte),
        ('PrimaryAFPoint', c_ubyte),
        ('AFPointsUsed', c_ubyte * 29),
        ('AFImageWidth', c_ushort),
        ('AFImageHeight', c_ushort),
        ('AFAreaXPposition', c_ushort),
        ('AFAreaYPosition', c_ushort),
        ('AFAreaWidth', c_ushort),
        ('AFAreaHeight', c_ushort),
        ('ContrastDetectAFInFocus', c_ubyte),
        ('FlashSetting', c_char * 13),
        ('FlashType', c_char * 20),
        ('FlashExposureCompensation', c_ubyte * 4),
        ('ExternalFlashExposureComp', c_ubyte * 4),
        ('FlashExposureBracketValue', c_ubyte * 4),
        ('FlashMode', c_ubyte),
        ('FlashExposureCompensation2', c_char),
        ('FlashExposureCompensation3', c_char),
        ('FlashExposureCompensation4', c_char),
        ('FlashSource', c_ubyte),
        ('FlashFirmware', c_ubyte * 2),
        ('ExternalFlashFlags', c_ubyte),
        ('FlashControlCommanderMode', c_ubyte),
        ('FlashOutputAndCompensation', c_ubyte),
        ('FlashFocalLength', c_ubyte),
        ('FlashGNDistance', c_ubyte),
        ('FlashGroupControlMode', c_ubyte * 4),
        ('FlashGroupOutputAndCompensation', c_ubyte * 4),
        ('FlashColorFilter', c_ubyte),
    ]


class libraw_olympus_makernotes_t(Structure):

    _fields_ = [
        ('OlympusCropID', c_int),
        ('OlympusFrame', c_ushort * 4),
        ('OlympusSensorCalibration', c_int * 2),
        ('FocusMode', c_ushort * 2),
        ('AutoFocus', c_ushort),
        ('AFPoint', c_ushort),
        ('AFAreas', c_uint * 64),
        ('AFPointSelected', c_double * 5),
        ('AFResult', c_ushort),
        ('ImageStabilization', c_uint),
        ('ColorSpace', c_ushort),
    ]


class libraw_pentax_makernotes_t(Structure):

    _fields_ = [
        ('FocusMode', c_ushort),
        ('AFPointMode', c_ubyte),
        ('AFPointSelected', c_ushort),
        ('AFPointsInFocus', c_uint),
        ('DriveMode', c_ubyte * 4),
        ('SRResult', c_ubyte),
        ('ShakeReduction', c_ubyte),
    ]


class libraw_sony_info_t(Structure):

    _fields_ = [
        ('SonyCameraType', c_ushort),
    ]


class libraw_makernotes_t(Structure):

    _fields_ = [
        ('canon', libraw_canon_makernotes_t),
        ('fuji', libraw_fuji_info_t),
        ('olympus', libraw_olympus_makernotes_t),
        ('sony', libraw_sony_info_t),
    ]


class libraw_shootinginfo_t(Structure):

    _fields_ = [
        ('DriveMode', c_short),
        ('FocusMode', c_short),
        ('MeteringMode', c_short),
        ('AFPoint', c_short),
        ('ExposureMode', c_short),
        ('ImageStabilization', c_short),
        ('BodySerial', c_char * 64),
        ('InternalBodySerial', c_char * 64),
    ]


class libraw_custom_camera_t(Structure):

    _fields_ = [
        ('fsize', c_uint),
        ('rw', c_ushort),
        ('rh', c_ushort),
        ('lm', c_ubyte),
        ('tm', c_ubyte),
        ('rm', c_ubyte),
        ('bm', c_ubyte),
        ('lf', c_ubyte),
        ('cf', c_ubyte),
        ('max', c_ubyte),
        ('flags', c_ubyte),
        ('t_make', c_char * 10),
        ('t_model', c_char * 20),
        ('offset', c_ushort)
    ]


class libraw_data_t(Structure):

    """
    A container which comprises the data structures that make up libraw's
    representation of a raw file.
    """
    _fields_ = [
        ('image', POINTER(c_ushort * 4)),
        ('sizes', libraw_image_sizes_t),
        ('idata', libraw_iparams_t),
        ('lens', libraw_lensinfo_t),
        ('makernotes', libraw_makernotes_t),
        ('shootinginfo', libraw_shootinginfo_t),
        ('params', libraw_output_params_t),
        ('progress_flags', c_uint),
        ('process_warnings', c_uint),
        ('color', libraw_colordata_t),
        ('other', libraw_imgother_t),
        ('thumbnail', libraw_thumbnail_t),
        ('rawdata', libraw_rawdata_t),
        ('parent_class', c_void_p),
    ]

class xtrans_params(Structure):

    _fields_ = [
        ('q_table', POINTER(c_char)),
        ('q_points', c_int * 5),
        ('max_bits', c_int),
        ('min_value', c_int),
        ('raw_bits', c_int),
        ('total_values', c_int),
        ('maxDiff', c_int),
        ('line_width', c_ushort),
    ]
