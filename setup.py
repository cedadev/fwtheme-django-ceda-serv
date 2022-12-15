#!/usr/bin/env python3

import os, re

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

if __name__ == "__main__":

    setup(
        name = 'fwtheme-django-ceda-serv',
        version = '1.5.2',
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
        extras_require = {
            'user_status': ['dj_security_middleware']
        },
    )
