"""
Django templatetags package.
"""

__author__ = "William Tucker"
__copyright__ = "Copyright 2018 UK Science and Technology Facilities Council"


from django import template
from django.conf import settings
from django.urls import reverse, resolve
from django.urls.exceptions import NoReverseMatch


DEFAULT_LOGIN_URL_NAME = "login"
DEFAULT_LOGOUT_URL_NAME = "logout"

LEGACY_MIDDLEWARE = "dj_security_middleware.middleware.DJSecurityMiddleware"

# Attempt imports from legacy security module
try:
    from dj_security_middleware.utils.request import \
        login_url as legacy_login, logout_url as legacy_logout
    _legacy_login_loaded = True
except ImportError:
    _legacy_login_loaded = False

_use_legacy_login = _legacy_login_loaded \
    and LEGACY_MIDDLEWARE in settings.MIDDLEWARE

# Template tags
register = template.Library()


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

    ## Authenticated user cookie requires .ceda.ac.uk domain
    ## Local versions will not allow login

    if _use_legacy_login and hasattr(request, "authenticated_user"):
        return request.authenticated_user.get("userid")
    elif hasattr(request, "user"):
        if request.user.is_authenticated:
            return request.user.username
    else:
        if '0.0' in request.build_absolute_uri():
            return 'local'


@register.simple_tag(takes_context=True)
def login_url(context):
    """ Return the application's login URL.
    Change the default by setting LOGIN_URL_NAME.
    """
    if _use_legacy_login:
        return legacy_login(context["request"])

    
    name = settings.LOGIN_URL_NAME if hasattr(settings, "LOGIN_URL_NAME") \
        else DEFAULT_LOGIN_URL_NAME
    
    try:
        auth_view = reverse(name)
        return auth_view + '?next=' + context['request'].path
    except NoReverseMatch:
        # No legacy login and no defined OIDC Login
        # Hence use default login url
        return "https://auth.ceda.ac.uk/account/signin/?r=" + context['request'].build_absolute_uri() # Need local website address fetch


@register.simple_tag(takes_context=True)
def logout_url(context):
    """ Return the application's logout URL.
    Change the default by setting LOGOUT_URL_NAME.
    """

    if _use_legacy_login:
        return legacy_logout(context["request"])

    name = settings.LOGOUT_URL_NAME if hasattr(settings, "LOGOUT_URL_NAME") \
        else DEFAULT_LOGOUT_URL_NAME
    try:
        auth_view = reverse(name)
        # next - not passed to logout system - bug
        return auth_view + '?next=' + context['request'].path
    except NoReverseMatch:
        # No legacy logout and no defined OIDC Logout
        # Hence use default logout url
        return "/?logout=" # Works in live versions
