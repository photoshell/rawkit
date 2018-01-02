# Usage: python examples/save_jpeg_using_pil.py src.CR2 dest.jpg
# Requires PIL (pip install pillow)
import sys
from PIL import Image
from rawkit.raw import Raw


src = sys.argv[1]
dest = sys.argv[2]


with Raw(filename=src) as raw:
    rgb_buffer = raw.to_buffer()

    # Convert the buffer from [r, g, b, r...] to [(r, g, b), (r, g, b)...]
    rgb_tuples = [
        tuple(rgb_buffer[i:i+3]) for i in range(0, len(rgb_buffer), 3)
    ]

    image = Image.new('RGB', [raw.metadata.width, raw.metadata.height])
    image.putdata(rgb_tuples)
    image.save(dest)
