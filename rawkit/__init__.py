"""Introduction
~~~~~~~~~~~~~~~

The :mod:`rawkit` module contains high-level APIs for manipulating raw photos
using the low-level :mod:`libraw` module (which in turn uses the even
lower-level LibRaw C library).

Eg. quickly processing a raw Canon CR2 file without using the camera white
balance and saving it as a PPM image might look like this:

.. sourcecode:: python

    from rawkit.raw import Raw
    from rawkit.options import WhiteBalance

    with Raw(filename='some/raw/image.CR2') as raw:
      raw.options.white_balance = WhiteBalance(camera=False, auto=True)
      raw.save(filename='some/destination/image.ppm')
"""

VERSION = '0.6.0'
"""
The current version of the `rawkit` package.
"""
