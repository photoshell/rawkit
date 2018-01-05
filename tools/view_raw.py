#! /usr/bin/env python
# Usage: tools/view_raw.py /path/to/raw/file
import sys

import matplotlib.pyplot as plt

from rawkit.raw import Raw

with Raw(filename=sys.argv[1]) as raw:
    plt.imshow(raw.as_array())
    plt.show()
