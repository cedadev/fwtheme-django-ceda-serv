"""
Django templatetags package.
"""

__author__ = "William Tucker"
__copyright__ = "Copyright 2018 UK Science and Technology Facilities Council"


from django import template
from django.conf import settings
from django.utils.http import urlencode

from fwtheme_django_ceda_serv.default_settings import USE_DJANGO_USER_STATUS, USE_CEDA_USER_STATUS

_security_module_loaded = True
try:
    from dj_security_middleware.middleware import LOGOUT, login_service, redirect_field_name
except ImportError:
    _security_module_loaded = False


# Template tags
register = template.Library()


def _django_status_enabled():
    """Return True if the application is configured to show user status for Django users"""
    
    return getattr(settings, 'USE_DJANGO_USER_STATUS', USE_DJANGO_USER_STATUS)


def _ceda_status_enabled():
    """Return True if the application is configured to accept CEDA authenticated users"""
    
    if not getattr(settings, 'USE_CEDA_USER_STATUS', USE_CEDA_USER_STATUS):
        return False
    
    return _security_module_loaded


@register.simple_tag
def show_user_status():
    """Return True if the application is configured to use the user_status block"""
    
    return _django_status_enabled() or _ceda_status_enabled()


@register.simple_tag(takes_context=True)
def show_ceda_status(context):
    """Return True if CEDA user status elements should be displayed
    
    Checks current user authentication and application settings.
    """
    
    request = context['request']
    if _ceda_status_enabled():
        if _django_status_enabled():
            if hasattr(request, 'authenticated_user') or not request.user.is_authenticated:
                return True
        else:
            return True
    
    return False


@register.simple_tag(takes_context=True)
def get_userid(context):
    """Return the user's ID if logged in
    
    Value is parsed from the user's login cookie.
    """
    
    request = context['request']
    
    if _django_status_enabled() and request.user.is_authenticated:
        return request.user.username
    
    elif hasattr(request, 'authenticated_user'):
        return request.authenticated_user.get('userid')


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
def logout_url(context):
    """Return the application's logout URL"""
    
    request = context['request']
    query_dict = request.GET.copy()
    query_dict[LOGOUT] = ''
    
    query_string = query_dict.urlencode()
    url = '{0}?{1}'.format(request.path, query_string)
    
    return url
