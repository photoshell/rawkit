[![Build status](https://api.travis-ci.org/photoshell/rawkit.svg?branch=master)](https://travis-ci.org/photoshell/rawkit)
[![Coverage Status](https://coveralls.io/repos/photoshell/rawkit/badge.svg)](https://coveralls.io/r/photoshell/rawkit)

# rawkit

`rawkit` (pronounced rocket) is a LibRaw binding for Python inspired by the Wand API.

## Usage

```python
from rawkit.raw import Raw

with Raw(filename='some/raw/image.CR2') as raw:
	raw.save(filename='some/destination/image.ppm')
```
