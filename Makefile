REBUILD_FLAG =
VENV=env
BIN=$(VENV)/bin
ACTIVATE=source $(BIN)/activate

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
	find . -iname '*.pyc' | xargs rm -f
	rm -rf .tox
	rm -rf $(VENV)
	rm -rf dist
	$(MAKE) -C docs $@

.PHONY: gendoc
docs: docs/*.rst
	$(ACTIVATE); $(MAKE) -C $@ html

docs/*.rst: *.py $(VENV)
	$(ACTIVATE); sphinx-apidoc -o docs/source rawkit docs
