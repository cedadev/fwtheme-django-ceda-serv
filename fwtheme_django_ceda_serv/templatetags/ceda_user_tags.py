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

    if "request" in context:
        request = context["request"]
    else:
        return None

    ## Authenticated user cookie requires .ceda.ac.uk domain
    ## Local versions will not allow login
    
    # Legacy login or OIDC login
    if _use_legacy_login and hasattr(request, "authenticated_user"):
        if settings.DEBUG:
            print('auth_user')
        return request.authenticated_user.get("userid")
    elif hasattr(request, "user"):
        if settings.DEBUG:
            print('user')
        if request.user.is_authenticated:
            return request.user.username
    else:
        if settings.DEBUG:
            print('No user')
        return None


@register.simple_tag(takes_context=True)
def login_url(context):
    """ Return the application's login URL.
    Change the default by setting LOGIN_URL_NAME.
    """
    url = DEFAULT_LOGIN_URL_NAME

    # Handle no login
    if hasattr(settings,"DISABLE_LOGIN"):
        if settings.DISABLE_LOGIN:
            return None

    # Handle Legacy
    if _use_legacy_login:
        if "request" in context:
            return legacy_login(context["request"])
        else:
            return None

    # Handle non-default login url
    if hasattr(settings, "LOGIN_URL_NAME"):
        url = settings.LOGIN_URL_NAME
    else:
        url = DEFAULT_LOGIN_URL_NAME
    
    try:
        auth_view = reverse(url)
        if hasattr(context,'request'):
            return auth_view + '?next=' + context['request'].path
        else:
            return auth_view
    except NoReverseMatch:
        # No legacy login and no defined OIDC Login
        return None
    except:
        return auth_view


@register.simple_tag(takes_context=True)
def logout_url(context):
    """ Return the application's logout URL.
    Change the default by setting LOGOUT_URL_NAME.
    """

    if _use_legacy_login:
        if "request" in context:
            return legacy_logout(context["request"])
        else:
            return None

    name = settings.LOGOUT_URL_NAME if hasattr(settings, "LOGOUT_URL_NAME") \
        else DEFAULT_LOGOUT_URL_NAME
    try:
        auth_view = reverse(name)
        # next - not passed to logout system - bug
        if hasattr(context,'request'):
            return auth_view + '?next=' + context['request'].path
        else:
            return auth_view
    except NoReverseMatch:
        # No legacy logout and no defined OIDC Logout
        # Hence use default logout url
        return "/?logout=" # Works in live versions
