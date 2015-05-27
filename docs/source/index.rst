rawkit
======

.. image:: https://secure.travis-ci.org/photoshell/rawkit.svg?branch=master
   :alt: Build Status
   :target: https://travis-ci.org/photoshell/rawkit

.. image:: https://img.shields.io/coveralls/photoshell/rawkit.svg?style=flat
   :alt: Test Coverage Status
   :target: https://coveralls.io/r/photoshell/rawkit

``rawkit`` (pronounced `rocket`) is a :mod:`ctypes`-based LibRaw_ binding for
Python inspired by the Wand_ API. ::

    from rawkit.raw import Raw
    from rawkit.options import WhiteBalance

    with Raw(filename='some/raw/image.CR2') as raw:
      raw.options.white_balance = WhiteBalance(camera=False, auto=True)
      raw.save(filename='some/destination/image.ppm')

.. _LibRaw: http://www.libraw.org/
.. _Wand: http://docs.wand-py.org

Requirements
------------

- Python

  - CPython 2.7+
  - CPytohn 3.3+
  - PyPy 2.5+
  - PyPy3 2.4+

- LibRaw

  - LibRaw 0.16.x (API version 10)

Installing rawkit
-----------------

First, you'll need to install LibRaw:

  - `libraw` on Arch_
  - `LibRaw` on Fedora_ 21+
  - `libraw10` on Ubuntu_ Utopic+
  - `libraw-bin` on Debian_ Jessie+
.. TODO: OS X with homebrew?

Now you can fetch rawkit from PyPi_:

.. sourcecode:: bash

    $ pip install rawkit

.. _Arch: https://www.archlinux.org/packages/extra/x86_64/libraw/
.. _Fedora: https://apps.fedoraproject.org/packages/LibRaw
.. _Ubuntu: http://packages.ubuntu.com/utopic/libraw10
.. _Debian: https://packages.debian.org/stable/graphics/libraw-bin
.. _PyPi: https://pypi.python.org/pypi/rawkit

API Reference
-------------

.. toctree::
   :maxdepth: 2

   api/rawkit

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

