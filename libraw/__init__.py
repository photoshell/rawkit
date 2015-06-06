from libraw.bindings import LibRaw

libraw = LibRaw()
"""
A handle to the LibRaw binary installed on the end users machine.

This should always be imported first by anything that wants to use `libraw`:

.. sourcecode:: python

    from libraw import libraw
"""
