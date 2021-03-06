# Makefile for Sphinx documentation
#

SPHINXBUILD   = sphinx-build
BUILDDIR      = docs/build

# User-friendly check for sphinx-build
ifeq ($(shell which $(SPHINXBUILD) >/dev/null 2>&1; echo $$?), 1)
$(error The '$(SPHINXBUILD)' command was not found. Make sure you have Sphinx installed, then set the SPHINXBUILD environment variable to point to the full path of the '$(SPHINXBUILD)' executable. Alternatively you can add the directory with the executable to your PATH. If you don't have Sphinx installed, grab it from http://sphinx-doc.org/)
endif

.PHONY: help clean html

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html       to make standalone HTML files"

clean:
	rm -rf $(BUILDDIR)/*

html:
	cp AUTHORS.rst docs/source
	cp HISTORY.rst docs/source
	cp README.rst docs/source
	sphinx-apidoc -f -o docs/source scout_api
	sphinx-build -b html -d $(BUILDDIR)/doctrees docs/source $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

upload:
	python setup.py sdist upload
	python setup.py bdist_wheel upload
	python setup.py upload_sphinx

upload_doc:
	python setup.py upload_sphinx
