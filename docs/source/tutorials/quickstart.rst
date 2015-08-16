Getting Started
===============

If you read the beginning of this documentation, you've seen one example of
using rawkit already. Let's see an even simpler form of it:

.. sourcecode:: python

    from rawkit.raw import Raw

    with Raw(filename='some/raw/image.CR2') as raw:
      raw.save(filename='some/destination/image.ppm')

This constructs a :class:`rawkit.raw.Raw` object which loads the file
``image.CR2`` as a context manager and then saves the output file
``image.ppm``. One of the design goals of rawkit is "have sane defaults", which
means that this is pretty much all you need to do to get a decent looking
photo. Of course, you probably want to customize how your photo is developed.
For this you can use :mod:`rawkit.options`.

The ``Raw`` object you created has a :class:`rawkit.options.Options` object
already with the aforementioned sane defaults, so instead of constructing a new
object let's just modify the existing one to tweak the white balance and a few
other options:

.. sourcecode:: python

    from rawkit.raw import Raw
    from rawkit.options import WhiteBalance, colorspaces, gamma_curves

    with Raw(filename='some/raw/image.CR2') as raw:
      raw.options.white_balance = WhiteBalance(camera=False, auto=True)
      raw.options.colorspace = colorspaces.adobe_rgb
      raw.options.gamma = gamma_curves.adobe_rgb
      raw.save(filename='some/destination/image.ppm')

By default rawkit uses the white balance written to the raw file by your camera
(if available) and falls back to automatically guessing at the white balance if
no camera specified white balance is available. However, here we've constructed
a new :class:`rawkit.options.WhiteBalance` object which does not attempt to use
the camera white balance (note that ``WhiteBalance`` objects are immutable, so
you'll always need to construct a new one if you're changing the white
balance). We've also changed the colorspace to Adobe RGB instead of the default
sRGB, and changed the gamma curve to use the corrective power function for the
Adobe RGB colorspace.

Lots of other options can be set. A full list can be found in the API
documentation for the :mod:`rawkit.options` module.

Of course, we probably don't want to process just one raw file. A common
photography workflow is to do some basic level of processing to lots of files
at once (eg. an entire days worth of shooting) and then go back and tweak
individual photos as necessary. To do this, we can construct our own options
object and reuse it:

.. sourcecode:: python

    import sys

    from rawkit.raw import Raw
    from rawkit.options import WhiteBalance, colorspaces, gamma_curves
    from rawkit.options import Options

    opts = Options({
      'white_balance': WhiteBalance(camera=False, auto=True),
      'colorspace': colorspaces.adobe_rgb,
    })

    opts.gamma = gamma_curves.adobe_rgb


    for rawfile in sys.argv[1:]
      with Raw(filename=rawfile) as raw:
        raw.options = opts
        raw.save(filename='{}.ppm'.format(rawfile))

As you can see, two methods for setting options on an ``Options`` object are
presented here: via a dict passed to the constructor, or by manually setting
the properties. Because the dict method tolerates arbitrary fields, you must be
very careful not to make a typo. Eg. setting:

.. sourcecode:: python

    opts = Options({
      'colourspace': colorspaces.adobe_rgb,
      'white_blaance': WhiteBalance(greybox=[1034, 1058, 1096, 1085])
    })

will run without error, but there will be no difference to your output photos.
However, trying to set options via:

.. sourcecode:: python

    opts = Options()
    opts.colourspace = colorspaces.adobe_rgb
    opts.white_blaance = WhiteBalance(greybox=[1034, 1058, 1096, 1085])

Will result in an :class:`AttributeError`. This is the recommended method for
manually setting options because it will fail early and loudly!

Now that we've seen the basics (loading and saving raw files and setting
options), let's turn our simple example into something useful: A program which
will take in the name of one or more raw files and attempt to save them as
standard TIFF files. First, we'll snag the arguments and add a bit of error
checking (we'll also get rid of the options and just use the defaults for now):

.. sourcecode:: python

    import sys

    from libraw.errors import FileUnsupported
    from rawkit.errors import InvalidFileType
    from rawkit.raw import Raw

    if __name__ == "__main__":

      for rawfile in sys.argv[1:]:
        try:
          with Raw(filename=rawfile) as raw:
            outfile = '{}.tiff'.format(rawfile)
            raw.save(filename=outfile)
            print(
              'Wrote file: "{}".'.format(
                outfile
              )
            )
        except (InvalidFileType, FileUnsupported):
            print(
              'WARNING: File "{}" could not be processed.'.format(
                rawfile
              ),
              file=sys.stderr
            )

Of course, while this works, it's still a bit slow. Let's add a thread pool to
the mix and process multiple raw files at once (not that this has anything to
do with actually using rawkit, but we might as well do things right):

.. sourcecode:: python

   import concurrent.futures
   import os
   import sys

   from libraw.errors import FileUnsupported
   from rawkit.errors import InvalidFileType
   from rawkit.raw import Raw

   def develop_photo(rawfile):
       with Raw(filename=rawfile) as raw:
           outfile = '{}.tiff'.format(rawfile)
           raw.save(filename=outfile)
           return outfile

   if __name__ == "__main__":

       with concurrent.futures.ThreadPoolExecutor(max_workers=(
           (os.cpu_count() or 2) * 2)) as executor:
           develop_futures = {executor.submit(develop_photo, raw): raw for raw
               in sys.argv[1:]}
           for future in concurrent.futures.as_completed(develop_futures):
               raw = develop_futures[future]
               try:
                   data = future.result()
               except (InvalidFileType, FileUnsupported):
                   print(
                     'WARNING: File "{}" could not be processed'.format(raw),
                     file=sys.stderr
                   )
               else:
                   print('Wrote file: "{}"'.format(data))


That's it, you've made a useful application which uses rawkit to develop raw
photos! For a slightly more interesting example, take a look at the source to
photoREPL_, an experimental interface for editing photos from the command line.

.. _photoREPL: https://github.com/photoshell/photorepl
