""":mod:`libraw.errors` --- Pythonic error handling for LibRaw
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


class UnspecifiedError(Exception):
    pass


class FileUnsupported(Exception):
    pass


class RequestForNonexistentImage(Exception):
    pass


class OutOfOrderCall(Exception):
    pass


class NoThumbnail(Exception):
    pass


class UnsupportedThumbnail(Exception):
    pass


class InputClosed(Exception):
    pass


class InsufficientMemory(Exception):
    pass


class DataError(Exception):
    pass


class IOError(Exception):
    pass


class CancelledByCallback(Exception):
    pass


class BadCrop(Exception):
    pass


def check_call(exit_code):
    if exit_code is not 0:
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
            -100010: CancelledByCallback,
            -100011: BadCrop
        }[exit_code]
