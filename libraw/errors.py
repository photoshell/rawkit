""":mod:`libraw.errors` --- Pythonic error handling for LibRaw
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from ctypes import c_int


class c_error(c_int):

    """
    An error type for LibRaw (since LibRaw errors are ints and you can't
    distinguish between functions that return an error and functions that
    return an int that doesn't code for an error).
    """


class LibRawError(Exception):

    """
    A base exception class from which all other exceptions that originate in
    LibRaw inherit.
    """


class UnspecifiedError(LibRawError):

    """
    Something bad happened, but we don't know what.
    """


class FileUnsupported(LibRawError):

    """
    The file is not a raw file or is from an unsupported camera.
    """


class RequestForNonexistentImage(LibRawError):

    """
    The image file directory in the raw file which you are trying to access
    does not contain an image.
    """


class OutOfOrderCall(LibRawError):

    """
    A LibRaw function depends on another function being called first and was
    invoked out of order.
    """


class NoThumbnail(LibRawError):

    """
    The raw file does not contain a thumbnail.
    """


class UnsupportedThumbnail(LibRawError):

    """
    The thumbnail format is not supported.
    """


class InputClosed(LibRawError):

    """
    There is no input stream, or the input stream has been closed.
    """


class InsufficientMemory(LibRawError):

    """
    Memory allocation failed.
    """


class DataError(LibRawError):

    """
    Data unpacking failed.
    """


class CanceledByCallback(LibRawError):

    """
    Image processing was canceled because the progress callback requested it.
    """


class BadCrop(LibRawError):

    """
    The cropping coordinates specified are invalid (eg. the top left corner of
    the cropping rectangle is outside the image).
    """


def check_call(exit_code, func, arguments):
    """
    Throws a Python error which corresponds to the given LibRaw exit code.

    Args:
        exit_code (int): An exit code returned by a LibRaw function.

    Raises:
        UnspecifiedError: We're not sure what happened.
        FileUnsupported: The file is not a raw file that we recognize.
        RequestForNonexistentImage: The given IFD does not contain an image.
        OutOfOrderCall: Something was called out of order (eg. before data was
                        unpacked)
        NoThumbnail: The image does not have a thumbnail.
        UnsupportedThumbnail: The embedded thumbnail format is unsupported.
        InputClosed: The input stream has been closed.
        InsufficientMemory: We're out of memory.
        DataError: The unpacking step failed.
        IOError: Reading was interrupted (or the file is corrupt).
        CanceledByCallback: A callback canceled the operation.
        BadCrop: The crop range was invalid.
    """

    if func.restype is c_error:
        raise_if_error(exit_code.value)

    return exit_code


def raise_if_error(error_code):
    """
    :func:`raise_if_error` raises a meaningful exception that corresponds to the
    given LibRaw integer return value.

    Args:
        error_code (int): An exit code returned by a LibRaw function.

    Raises:
        UnspecifiedError: We're not sure what happened.
        FileUnsupported: The file is not a raw file that we recognize.
        RequestForNonexistentImage: The given IFD does not contain an image.
        OutOfOrderCall: Something was called out of order (eg. before data was
                        unpacked)
        NoThumbnail: The image does not have a thumbnail.
        UnsupportedThumbnail: The embedded thumbnail format is unsupported.
        InputClosed: The input stream has been closed.
        InsufficientMemory: We're out of memory.
        DataError: The unpacking step failed.
        IOError: Reading was interrupted (or the file is corrupt).
        CanceledByCallback: A callback canceled the operation.
        BadCrop: The crop range was invalid.
    """
    if error_code != 0:
        raise {
            -1: UnspecifiedError,
            -2: FileUnsupported,
            -3: RequestForNonexistentImage,
            -4: OutOfOrderCall,
            -5: NoThumbnail,
            -6: UnsupportedThumbnail,
            -7: InputClosed,
            -100007: InsufficientMemory,
            -100008: DataError,
            -100009: IOError,
            -100010: CanceledByCallback,
            -100011: BadCrop
        }[error_code]
