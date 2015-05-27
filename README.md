[![Docs status](https://readthedocs.org/projects/rawkit/badge/?version=latest)](https://rawkit.readthedocs.org/en/latest/)
[![Build status](https://api.travis-ci.org/photoshell/rawkit.svg?branch=master)](https://travis-ci.org/photoshell/rawkit)
[![Coverage status](https://coveralls.io/repos/photoshell/rawkit/badge.svg)](https://coveralls.io/r/photoshell/rawkit)

# rawkit

`rawkit` (pronounced rocket) is a LibRaw binding for Python inspired by the
Wand API. For more info, see the [docs][docs].

## Usage

```python
from rawkit.raw import Raw

with Raw(filename='some/raw/image.CR2') as raw:
	raw.save(filename='some/destination/image.ppm')
```

[docs]: https://photoshell.github.io/rawkit/
