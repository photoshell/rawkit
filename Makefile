REBUILD_FLAG =
VENV=env
BIN=$(VENV)/bin
ACTIVATE=. $(BIN)/activate

.PHONY: all
all: test build pre-commit

.PHONY: pre-commit
pre-commit: .git/hooks/pre-commit
.git/hooks/pre-commit: .pre-commit-config.yaml $(VENV)
	$(ACTIVATE); pre-commit install

$(VENV): $(VENV)/bin/activate

$(VENV)/bin/activate: requirements-dev.txt requirements-test.txt
	test -d $(VENV) || virtualenv -p /usr/bin/python3 $(VENV)
	$(ACTIVATE); pip install -r requirements-dev.txt
	touch $(BIN)/activate


.PHONY: test
test: $(VENV)
	$(ACTIVATE); tox $(REBUILD_FLAG)

.PHONY: stress-test
stress-test: $(VENV)
	$(ACTIVATE); INPUT=$(INPUT) tox -c tox-stress.ini $(REBUILD_FLAG)

dist/*.whl: setup.py rawkit/*.py
	python setup.py bdist_wheel

dist/*.tar.gz: setup.py rawkit/*.py
	python setup.py sdist bdist

.PHONY: wheel
wheel: dist/*.whl

.PHONY: dist
dist: dist/*.tar.gz

.PHONY: build
build: pre-commit wheel dist

.PHONY: upload
upload: build test
	python setup.py sdist bdist bdist_wheel upload

.PHONY: clean
clean:
	$(ACTIVATE); $(MAKE) -C docs $@
	find . -iname '*.pyc' | xargs rm -f
	rm -rf docs/source/api/*
	rm -rf .tox
	rm -rf dist
	rm -rf $(VENV)

.PHONY: docs
docs: epub html

.PHONY: html
html: docs/source/api/rawkit.rst docs/source/api/libraw.rst docs/source/* docs/source/_static/*
	$(ACTIVATE); $(MAKE) -C docs $@

.PHONY: epub
epub: docs/source/api/rawkit.rst docs/source/api/libraw.rst
	$(ACTIVATE); $(MAKE) -C docs $@

docs/source/api/rawkit.rst: rawkit/*.py $(VENV)
	$(ACTIVATE); sphinx-apidoc -M -o docs/source/api rawkit docs

docs/source/api/libraw.rst: libraw/*.py $(VENV)
	$(ACTIVATE); sphinx-apidoc -M -o docs/source/api libraw docs
