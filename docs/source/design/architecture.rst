Architecture
============

When we talk about "rawkit" we're actually talking about an entire stack of
libraries which work together to give you a simple way to work with raw photo
data in Python. However, under the hood, rawkit comprises three separate
libraries which operate in a teired structure:


.. only:: builder_html

   .. raw:: html
      :file: ../art/architecture.svg

.. only:: not builder_html

   .. image:: ../art/architecture.png
      :alt: rawkit architecture diagram

The bottom layer is the LibRaw_ C library, which is used to actually extract
data from raw photo files, and to do basic processing. LibRaw is not actually
bundled with rawkit, and must already be installed on the end users computer.
The next layer, also called :class:`libraw`, is a low-level Python library
which uses ctypes_ to link to the LibRaw C code. This library, while written in
Python, generally just looks and acts like the lower-level C code, albeit with
slightly more Pythonic error handling and a few helper functions to make it
easier to use from within Python. However, you generally shouldn't use libraw.
Instead, you should use the highest level methods available, :mod:`rawkit`.
The actual rawkit namespace provides a module which builds on libraw to provide
a fully Pythonic interface to the underlying library (eg. :class:`rawkit.Raw`
objects, context managers, an API for setting options, etc.). If at all
possible, you should use the rawkit module in your applications, but the libraw
module is still exposed in case you need to dig down and perform some
functionality that is not exposed by rawkit.

More details about each tier can be found below.

LibRaw
------

The foundation of the entire rawkit stack is the LibRaw_ C library. LibRaw is
maintained by LibRaw, LLC. and does the actual grunt work of loading raw files,
extracting data, and developing photos via its dcraw emulation layer. It is the
only real dependency of rawkit and must be installed on the end-users
computer before this library will actually work.

libraw
------

The :mod:`libraw` module is a set of Python bindings which use ctypes_ to
talk to the LibRaw library on the users system. The libraw module provides very
low level bindings that mostly juts mimic the C structs  present in LibRaw. It
also defines function and method arguments and return types, allows you to use
Python functions as callbacks to LibRaw events, maps LibRaw error codes to
actual Python exceptions, and handles the actual linking with ``libraw.so`` (or
the equivalent library on your system). In general, you should never have to
call libraw directly. Instead, you should use the higher level API's provided
by :mod:`rawkit`.

rawkit
------

The :mod:`rawkit` module is the highest level part of the rawkit architecture.
This module handles raw files in a Pythonic way by abstracting them to a
:class:`rawkit.Raw` object which acts as a context manager, and allowing you to
set options for how that raw file should be processed. It also contains a set
of utility functions (see :class:`rawkit.util`) for dealing with common
operations that may not be directly related to raw files (eg.  discovering
support for raw files, or getting a list of cameras supported by the linked
version of LibRaw).

.. _LibRaw: http://www.libraw.org/
.. _ctypes: https://docs.python.org/3/library/ctypes.html#module-ctypes
