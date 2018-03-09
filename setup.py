#!/usr/bin/env python3

import os, re

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

try:
    import ceda_theme.__version__ as version
except ImportError:
    # If we get an import error, find the version string manually
    version = "unknown"
    with open(os.path.join(here, 'fwtheme_django_ceda_serv', '__init__.py')) as f:
        for line in f:
            match = re.search('__version__ *= *[\'"](?P<version>.+)[\'"]', line)
            if match:
                version = match.group('version')
                break

with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

if __name__ == "__main__":

    setup(
        name = 'fwtheme-django-ceda-serv',
        version = version,
        description = 'Framework-level theme for Django customised for CEDA Services app using bootstrap 4',
        long_description = README,
        classifiers = [
            "Programming Language :: Python",
            "Framework :: Django",
            "Topic :: Internet :: WWW/HTTP",
            "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
        author = 'Matt Pritchard',
        author_email = 'matt.pritchard@stfc.ac.uk',
        url = 'https://github.com/cedadev/fwtheme-django-ceda-serv',
        keywords = 'web django theme bootstrap',
        packages = find_packages(),
        include_package_data = True,
        zip_safe = False,
        install_requires = [ ],
        extras_require = { },
    )
