# rawkit

`rawkit` (pronounced rocket) is a LibRaw binding for Python inspired by the Wand API.

## Usage

```python
from rawkit.raw import Raw

with Raw(filename='some/raw/image.CR2') as raw:
	raw.save(filename='some/destination/image.ppm')
```
