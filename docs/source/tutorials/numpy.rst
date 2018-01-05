Using Rawkit with NumPy
=======================

Rawkit can be used to easily access raw data as NumPy arrays.

.. sourcecode:: python

    from rawkit.raw import Raw

    with Raw(filename='some/raw/image.CR2') as raw:
        pixels = raw.as_array()
        color_filter_array = raw.color_filter_array

        # Randomly chosen pixel
        x = 307
        y = 123

        intensity = pixels[y][x]
        color = color_filter_array[y % 2][x % 2]
        message = 'The pixel at {x},{y} has intensity {i} and color {c}'

        print(message.format(
            x=x,
            y=y,
            i=intensity,
            c=color,
        ))
