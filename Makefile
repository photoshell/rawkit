REBUILD_FLAG =
RUN=pipenv run
APIDOCS=docs/source/api
DOCSRC=$(APIDOCS)/modules.rst docs/source/* docs/source/_static/*

.PHONY: all
all: test build pre-commit

.PHONY: pipenv
pipenv:
	pipenv install --dev --ignore-pipfile

.PHONY: pre-commit
pre-commit: .git/hooks/pre-commit pipenv

.git/hooks/pre-commit: .pre-commit-config.yaml
	$(RUN) pre-commit install

.PHONY: test
test: pipenv
	$(RUN) tox $(REBUILD_FLAG)

.PHONY: stress-test
stress-test: pipenv
	$(RUN) INPUT=$(INPUT) tox -c tox-stress.ini $(REBUILD_FLAG)

dist/*.whl: setup.py rawkit/*.py
	$(RUN) python setup.py bdist_wheel

dist/*.tar.gz: setup.py rawkit/*.py
	$(RUN) python setup.py sdist bdist

.PHONY: wheel
wheel: dist/*.whl

.PHONY: dist
dist: dist/*.tar.gz

.PHONY: build
build: pipenv pre-commit wheel dist

.PHONY: upload
upload: clean
	$(RUN) python setup.py sdist bdist bdist_wheel upload

.PHONY: clean
clean:
	-$(RUN) $(MAKE) -C docs $@
	find . -iname '*.pyc' | xargs rm -f
	find . -iname '__pycache__' -type d | xargs rm -rf
	rm -rf .tox
	rm -rf build
	rm -rf dist

.PHONY: docs
docs: epub html

.PHONY: html
html: $(DOCSRC)
	$(RUN) $(MAKE) -C docs $@

.PHONY: epub
epub: $(DOCSRC)
	$(RUN) $(MAKE) -C docs $@

$(APIDOCS)/modules.rst: rawkit/*.py libraw/*.py
	$(RUN) sphinx-apidoc -f -E -M -o $(APIDOCS) -H Contents . docs tests setup.py
