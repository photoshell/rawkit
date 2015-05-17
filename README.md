# rawkit

`rawkit` (pronounced rocket) is a LibRaw binding for Python inspired by the Wand API.

## Usage

```
from rawkit.raw import Raw

with Raw(filename='some/raw/image.CR2') as raw:
	raw.process()
	raw.save(filename='some/destination/image.ppm')
```
