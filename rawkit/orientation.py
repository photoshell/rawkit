# EXIF 2.3:
#
# 1 - The 0th row is at the visual top of the image, and the 0th
#     column is the visual left-hand side.
# 2 - The 0th row is at the visual top of the image, and the 0th
#     column is the visual right-hand side.
# (mirror horizontal)
# 3 - The 0th row is at the visual bottom of the image, and the
#     0th column is the visual right-hand side.
# 4 - The 0th row is at the visual bottom of the image, and the
#     0th column is the visual left-hand side.
# (mirrored vertical)
# 5 - The 0th row is the visual left-hand side of the image, and
#     the 0th column is the visual top.
# (
# 6 - The 0th row is the visual right-hand side of the image,
#     and the 0th column is the visual top.
# 7 - The 0th row is the visual right-hand side of the image,
#     and the 0th column is the visual bottom.
# 8 - The 0th row is the visual left-hand side of the image, and
#     the 0th column is the visual bottom.
exif_orientation_map = {
    # libraw: exif
    0: 1,  # No rotation
    1: 2,  # mirror horizontal
    2: 4,  # mirror vertical
    3: 3,  # 180-deg
    4: 5,  # 90ccw, mirror vertical
    5: 8,  # 90ccw
    6: 6,  # 90cw
    7: 7,  # 90cw, mirror vertical
}


def get_orientation(data):
    # TODO: find a way to handle mirrored images
    # See https://github.com/photoshell/rawkit/issues/120 for more context
    return exif_orientation_map.get(data.contents.sizes.flip, 1)
