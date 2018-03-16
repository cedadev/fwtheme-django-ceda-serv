# fwtheme-django-ceda-serv

Django app providing Django framework theme for Django-based web apps, themed for CEDA Services. Requires lower-level fwtheme-django.

## Installation

`fwtheme-django-ceda-serv` can be installed directly from Github using pip:

```
$ pip install git+https://github.com/cedadev/fwtheme-django-ceda-serv.git
```

In `settings.py`, this app should have an entry in INSTALLED_APPS *before* fwtheme_django for correct precedence, as its templates should override those of `fwtheme-django`. Similarly with orgtheme-ceda-serv and orgtheme:

```
    'fwtheme_django_ceda_serv',
    'fwtheme_django',
    'orgtheme_ceda_serv',
    'orgtheme',
```
