#! /usr/bin/env python
# Usage: tools/view_raw.py /path/to/raw/file
import sys

import matplotlib.pyplot as plt
import numpy as np

from rawkit.raw import Raw

with Raw(filename=sys.argv[1]) as raw:
    data = np.array(raw.raw_image())
    plt.imshow(data)
    plt.show()
