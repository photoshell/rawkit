import libraw.bindings

libraw = libraw.bindings.libraw
"""
A handle to the LibRaw binary installed on the end users machine.

This should always be imported first by anything that wants to use `libraw`:

.. sourcecode:: python

    from libraw import libraw
"""
