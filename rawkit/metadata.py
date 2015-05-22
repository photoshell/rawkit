""":mod:`rawkit.metadata` --- Metadata structures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from collections import namedtuple


Orientation = namedtuple('Orientation', [
    'landscape',
    'portrait',
])(0, 1)
"""
Represents the orientation of an image. Either `landscape` or `portrait`.
"""


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
"""
