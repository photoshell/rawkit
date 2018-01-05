exif_orientation_map = {
    0: 1,
    6: 6,
    3: 3,
    5: 8,
}


def get_orientation(data):
    # TODO: find a way to handle mirrored images
    # See https://github.com/photoshell/rawkit/issues/120 for more context
    return exif_orientation_map.get(data.contents.sizes.flip, 1)
