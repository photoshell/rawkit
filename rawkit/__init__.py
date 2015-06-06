VERSION = '0.1.0'
"""
The current version of the `rawkit` package.
"""

from libraw.bindings import LibRaw

_libraw = LibRaw()
"""
A handle to the LibRaw binary installed on the end users machine.
"""
