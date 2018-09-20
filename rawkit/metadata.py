""":mod:`rawkit.metadata` --- Metadata structures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from collections import namedtuple


Metadata = namedtuple('Metadata', [
    'aperture',
    'timestamp',
    'shutter',
    'flash',
    'focal_length',
    'height',
    'iso',
    'make',
    'model',
    'orientation',
    'width',
])
"""
Common metadata for a photo.

Orientation matches the values from the EXIF 2.3 specification:

1 - The 0th row is at the visual top of the image, and the 0th
    column is the visual left-hand side.
2 - The 0th row is at the visual top of the image, and the 0th
    column is the visual right-hand side.
3 - The 0th row is at the visual bottom of the image, and the
    0th column is the visual right-hand side.
4 - The 0th row is at the visual bottom of the image, and the
    0th column is the visual left-hand side.
5 - The 0th row is the visual left-hand side of the image, and
    the 0th column is the visual top.
6 - The 0th row is the visual right-hand side of the image,
    and the 0th column is the visual top.
7 - The 0th row is the visual right-hand side of the image,
    and the 0th column is the visual bottom.
8 - The 0th row is the visual left-hand side of the image, and
    the 0th column is the visual bottom.
"""
