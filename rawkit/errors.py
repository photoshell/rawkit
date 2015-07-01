""":mod:`rawkit.errors` --- Errors thrown by rawkit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These errors are thrown by various rawkit functions and methods when things go
wrong. They will only be raised by rawkit; for lower level errors raised by the
underlying libraw bindings, see :class:`libraw.errors`.
"""


class InvalidFileType(ValueError):

    """
    Raised when an invalid file type or file extension is passed to a rawkit
    method.
    """


class NoFileSpecified(ValueError):

    """
    Raised when the method or function excpects a `filename` argument, but no
    file name (or a value of `None`) was specified.
    """
