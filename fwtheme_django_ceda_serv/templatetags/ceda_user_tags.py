"""
Django templatetags package.
"""

__author__ = "William Tucker"
__copyright__ = "Copyright 2018 UK Science and Technology Facilities Council"


from django import template
from django.utils.http import urlencode

security_module_loaded = True
try:
    from dj_security_middleware.middleware import LOGOUT, REGISTRATION,\
        login_service, get_userid_from_request, get_openid_from_request, redirect_field_name
except ImportError:
    security_module_loaded = False


# Template tags
register = template.Library()


@register.simple_tag
def ceda_cookie_enabled():
    """Return True if the application can parse CEDA cookies
    
    Checks whether or not the dj_security_middleware package is available.
    """
    
    return security_module_loaded


@register.simple_tag(takes_context=True)
def userid_from_cookie(context):
    """Return the user's ID if logged in
    
    Value is parsed from the user's login cookie.
    """
    
    request = context['request']
    return get_userid_from_request(request)


@register.simple_tag(takes_context=True)
def openid_from_cookie(context):
    """Return the user's OpenID if logged in
    
    Value is parsed from the user's login cookie.
    """
    
    request = context['request']
    return get_openid_from_request(request)


@register.simple_tag(takes_context=True)
def login_url(context):
    """Return the application's login URL
    
    URL is determined by a setting.
    """
    
    request = context['request']
    query_string = {redirect_field_name(): request.build_absolute_uri()}
    query_string = urlencode(query_string)
    
    url = '{0}?{1}'.format(login_service(), query_string)
    return url


@register.simple_tag(takes_context=True)
def registration_url(context):
    """Return the application's logout URL"""
    
    request = context['request']
    query_string = urlencode(
        {REGISTRATION: ''}
    )
    
    url = '{0}?{1}'.format(request.get_full_path(), query_string)
    return url


@register.simple_tag(takes_context=True)
def logout_url(context):
    """Return the application's logout URL"""
    
    request = context['request']
    query_string = urlencode(
        {LOGOUT: ''}
    )
    
    url = '{0}?{1}'.format(request.get_full_path(), query_string)
    return url
