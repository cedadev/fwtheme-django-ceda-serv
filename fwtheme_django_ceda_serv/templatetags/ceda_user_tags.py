"""
Django templatetags package.
"""

__author__ = "William Tucker"
__copyright__ = "Copyright 2018 UK Science and Technology Facilities Council"


from django import template
from django.conf import settings
from django.shortcuts import reverse
from django.urls.exceptions import NoReverseMatch


LEGACY_MIDDLEWARE = "dj_security_middleware.middleware.DJSecurityMiddleware"

# Attempt imports from legacy security module
try:
    from dj_security_middleware.utils.request import \
        login_url as legacy_login, logout_url as legacy_logout
except ImportError:
    _legacy_login_loaded = False

_use_legacy_login = _legacy_login_loaded \
    and LEGACY_MIDDLEWARE in settings.MIDDLEWARE

# Template tags
register = template.Library()


@register.simple_tag
def show_user_status():
    """ Return True if the application is configured to use
    the user_status block
    """

    if _use_legacy_login:
        return True

    try:
        reverse("login")
        return True

    except NoReverseMatch:
        return False


@register.simple_tag
def logout_with_post():
    """ Determines whether or not to use HTTP POST when logging out.
    Default is True unless overridden by settings.LOGOUT_WITH_POST.
    """

    return settings.LOGOUT_WITH_POST \
        if hasattr(settings, "LOGOUT_WITH_POST") else True


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
    else:
        return reverse("login")


@register.simple_tag(takes_context=True)
def logout_url(context):
    """ Return the application's logout URL
    """

    if _use_legacy_login:
        return legacy_logout(context['request'])
    else:
        return reverse("logout")
