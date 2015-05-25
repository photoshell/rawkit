class LibrawUnspecifiedError(Exception):
    pass

class LibrawFileUnsupported(Exception):
    pass

class LibrawRequestForNonexistentImage(Exception):
    pass

class LibrawOutOfOrderCall(Exception):
    pass

class LibrawNoThumbnail(Exception):
    pass

class LibrawUnsupportedThumbnail(Exception):
    pass

class LibrawInputClosed(Exception):
    pass

class LibrawUnsufficientMemory(Exception):
    pass

class LibrawDataError(Exception):
    pass

class LibrawIOError(Exception):
    pass

class LibrawCancelledByCallback(Exception):
    pass

class LibrawBadCrop(Exception):
    pass

class UndefinedLibrawException(Exception):
    pass

def check_call(exit_code):
    try:
        if exit_code is not 0:
            raise {
                -1 : LibrawUnspecifiedError,
                -2 : LibrawFileUnsupported,
                -3 : LibrawRequestForNonexistentImage,
                -4 : LibrawOutOfOrderCall,
                -5 : LibrawNoThumbnail,
                -6 : LibrawUnsupportedThumbnail,
                -7 : LibrawInputClosed,
                -100007 : LibrawUnsufficientMemory,
                -100008 : LibrawDataError,
                -100009 : LibrawIOError,
                -100010 : LibrawCancelledByCallback,
                -100011 : LibrawBadCrop
                }[exit_code]
    except KeyError:
        # Libraw has given us an exit code that we don't know about
        raise UndefinedLibrawException(exit_code)
