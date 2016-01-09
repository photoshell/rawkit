rawkit
======

.. image:: https://badge.fury.io/py/rawkit.svg?
  :alt: Package Status
  :target: https://pypi.python.org/pypi/rawkit

.. image:: https://readthedocs.org/projects/rawkit/badge/?version=latest
   :alt: Docs Status
   :target: https://rawkit.readthedocs.org/en/latest/

.. image:: https://secure.travis-ci.org/photoshell/rawkit.svg?branch=master
   :alt: Build Status
   :target: https://travis-ci.org/photoshell/rawkit

.. image:: https://img.shields.io/coveralls/photoshell/rawkit.svg?style=flat
   :alt: Test Coverage Status
   :target: https://coveralls.io/r/photoshell/rawkit

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :alt: MIT License
   :target: https://github.com/photoshell/rawkit/blob/master/LICENSE

.. note::

   `rawkit` is still alpha quality software. Until it hits 1.0, it may undergo
   substantial changes, including breaking API changes.

``rawkit`` is a :mod:`ctypes`-based set of LibRaw_ bindings for Python inspired
by Wand_. It is licensed under the `MIT License`_.

.. sourcecode:: python

    from rawkit.raw import Raw
    from rawkit.options import WhiteBalance

    with Raw(filename='some/raw/image.CR2') as raw:
      raw.options.white_balance = WhiteBalance(camera=False, auto=True)
      raw.save(filename='some/destination/image.ppm')

.. _LibRaw: http://www.libraw.org/
.. _Wand: http://docs.wand-py.org
.. _MIT License: https://github.com/photoshell/rawkit/blob/master/LICENSE

Requirements
------------

- Python

  - CPython 2.7+
  - CPython 3.4+
  - PyPy 2.5+
  - PyPy3 2.4+

- LibRaw

  - LibRaw 0.16.x (API version 10)
  - LibRaw 0.17.x (API version 11)

While other versions of Python or LibRaw may work, only the versions listed
above are tested for compatibility.

Installing rawkit
-----------------

First, you'll need to install LibRaw:

  - `libraw` on Arch_
  - `LibRaw` on Fedora_ 21+
  - `libraw10` on Ubuntu_ Utopic+
  - `libraw-bin` on Debian_ Jessie+

Now you can fetch rawkit from PyPi_:

.. sourcecode:: bash

    $ pip install rawkit

.. _Arch: https://www.archlinux.org/packages/extra/x86_64/libraw/
.. _Fedora: https://apps.fedoraproject.org/packages/LibRaw
.. _Ubuntu: http://packages.ubuntu.com/utopic/libraw10
.. _Debian: https://packages.debian.org/stable/graphics/libraw-bin
.. _PyPi: https://pypi.python.org/pypi/rawkit

Getting Help
------------

Need help? Join the ``#photoshell`` channel on Freenode. As always, don't ask
to ask (just ask) and if no one is around: be patient, if you part before we
can answer there's not much we can do. Stick around if you can; we'd love it if
you'd pay it forward and help someone else in turn.

Tutorials
---------

.. toctree::
   :glob:
   :maxdepth: 1

   tutorials/*

Architecture and Design
-----------------------

.. toctree::
   :glob:
   :maxdepth: 1

   design/*

API Reference
-------------

The `rawkit` package provides two modules: `rawkit` and `libraw`. The `rawkit`
module provides a high-level Pythonic interface for developing raw photos,
while the `libraw` module provides a CTypes based interface for interacting
with the low-level LibRaw C APIs. Most of the time, developers will want to use
the `rawkit` module instead of using `libraw` directly.

.. toctree::
   :maxdepth: 1

   api/modules
   api/libraw
   api/rawkit

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

