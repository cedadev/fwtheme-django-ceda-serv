# fwtheme-django-ceda-serv

Django app providing Django framework theme for Django-based web apps, themed for CEDA Services. Requires lower-level fwtheme-django.

## Installation

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

## User Status

There are two ways to enable the CEDA user status menu in the banner:

1. If using cookie based CEDA authentication, you must install the [DJ Security Middleware](https://github.com/cedadev/dj-security-middleware) package and include the middleware in your settings:

   ```python
   MIDDLEWARE = [
       ...
       "dj_security_middleware.middleware.DJSecurityMiddleware",
   ]
   ```

2. If using standard Django authentication (e.g. with Django admin users or a custom authentication backend),
   you simply need to have reversable login and logout URLs included in your `urls.py`:

   ```python
   urlpatterns = [
       path("/login", LoginView.as_view(), name="login"),
       path("/logout", LoginView.as_view(), name="logout"),
   ]
   ```

   If you wish to use names other than "login" and "logout", you can declare them in settings. For example, if you are using
   the recommended [OIDC authentication backend for CEDA accounts](https://github.com/cedadev/django-oidc-extras), you would set your URLs like this:

   ```python
   LOGIN_URL_NAME = "oidc_authentication_init"
   LOGOUT_URL_NAME = "oidc_logout"
   ```

### Login with GET

While not recommended, it is possible to configure the user status block to include an HTTP GET call for logout, instead of a form POST:

```python
LOGOUT_WITH_POST = False
```

This setting is `True` by default.
