""":mod:`libraw.errors` --- Pythonic error handling for LibRaw
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


class UnspecifiedError(Exception):

    """
    Something bad happened, but we don't know what.
    """


class FileUnsupported(Exception):

    """
    The file is not a raw file or is from an unsupported camera.
    """


class RequestForNonexistentImage(Exception):

    """
    The image file directory in the raw file which you are trying to access
    does not contain an image.
    """


class OutOfOrderCall(Exception):

    """
    A LibRaw function depends on another function being called first and was
    invoked out of order.
    """


class NoThumbnail(Exception):

    """
    The raw file does not contain a thumbnail.
    """


class UnsupportedThumbnail(Exception):

    """
    The thumbnail format is not supported.
    """


class InputClosed(Exception):

    """
    There is no input stream, or the input stream has been closed.
    """


class InsufficientMemory(Exception):

    """
    Memory allocation failed.
    """


class DataError(Exception):

    """
    Data unpacking failed.
    """


class IOError(Exception):

    """
    The RAW file is either corrupt or reading was interrupted somehow.
    """


class CancelledByCallback(Exception):

    """
    Image processing was canceled because the progress callback requested it.
    """


class BadCrop(Exception):

    """
    The cropping coordinates specified are invalid (eg. the top left corner of
    the cropping rectangle is outside the image).
    """
