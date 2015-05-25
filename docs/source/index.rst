rawkit
======

``rawkit`` (pronounced `rocket`) is a :mod:`ctypes`-based LibRaw_ binding for
Python inspired by the Wand_ API. ::

    from rawkit.raw import Raw

    with Raw(filename='some/raw/image.CR2') as raw:
      raw.save(filename='some/destination/image.ppm')

.. _LibRaw: http://www.libraw.org/
.. _Wand: http://docs.wand-py.org

Contents
--------

.. toctree::
   :maxdepth: 2

   rawkit

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

