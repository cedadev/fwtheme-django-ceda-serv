"""
Django templatetags package.
"""

__author__ = "William Tucker"
__copyright__ = "Copyright 2018 UK Science and Technology Facilities Council"


from django import template
from django.conf import settings
from django.shortcuts import reverse


LEGACY_MIDDLEWARE = "dj_security_middleware.middleware.DJSecurityMiddleware"
DEFAULT_OIDC_BACKEND = "mozilla_django_oidc.auth.OIDCAuthenticationBackend"


_use_oidc_login = settings.USE_OIDC_LOGIN \
    if hasattr(settings, "USE_OIDC_LOGIN") else False
if not _use_oidc_login:
    _use_oidc_login = DEFAULT_OIDC_BACKEND in settings.AUTHENTICATION_BACKENDS

_use_legacy_login = not _use_oidc_login \
    and LEGACY_MIDDLEWARE in settings.MIDDLEWARE

# Imports from legacy security module
try:
    from dj_security_middleware.utils.request import \
        login_url as legacy_login, logout_url as legacy_logout
except ImportError:
    _security_module_loaded = False


# Template tags
register = template.Library()


@register.simple_tag
def show_user_status():
    """ Return True if the application is configured to use
    the user_status block
    """
    
    return _use_oidc_login or _use_legacy_login


@register.simple_tag(takes_context=True)
def get_userid(context):
    """ Value is parsed from the user's login cookie.
    Return the user's ID if logged in
    """

    request = context["request"]

    if _use_legacy_login and hasattr(request, "authenticated_user"):
        return request.authenticated_user.get("userid")

    elif request.user.is_authenticated:
        return request.user.username


@register.simple_tag(takes_context=True)
def login_url(context):
    """ Return the application's login URL.
    """

    if _use_legacy_login:
        return legacy_login(context['request'])
    elif _use_oidc_login:
        return reverse("oidc_authentication_init")
    else:
        return reverse("login")


@register.simple_tag(takes_context=True)
def logout_url(context):
    """ Return the application's logout URL
    """

    if _use_legacy_login:
        return legacy_logout(context['request'])
    elif _use_oidc_login:
        return reverse("oidc_logout")
    else:
        return reverse("logout")
