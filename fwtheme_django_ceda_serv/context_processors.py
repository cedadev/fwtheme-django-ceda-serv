from .default_settings import DC_TEMPLATES, DATACENTRES, BEACONS

from django.conf import settings


ACCOUNT_REGISTRATION_URL_DEFAULT = "https://accounts.ceda.ac.uk/realms/ceda/account/#/personal-info"
ACCOUNT_CONSOLE_URL_DEFAULT = "https://accounts.ceda.ac.uk/realms/ceda/account/#/personal-info"
ACCOUNT_SECURITY_URL_DEFAULT = "https://accounts.ceda.ac.uk/realms/ceda/account/#/personal-info"


def data_centre(request):
    """
    Determine which data centre template is extended
    by browse.html
    """
    location = 'extra_data_centres/'
    data_centre_template = 'fwtheme_django/layout.html'  # default template - NERC EDS Theme

    # fwtheme_django_ceda_serv version 1.5.3

    # Dynamic Data Centre processing
    dc = request.path.split('/')[1] # /ceda/ -> ['','ceda','...']
    if dc not in ['ceda','badc','neodc'] and dc in DATACENTRES:
        data_centre_template = location + DC_TEMPLATES[dc]    
    context = {
        "data_centre_template": data_centre_template,
        "data_centre": dc,
    }
    return context

def beacon(request):
    # Determine which beacon to use
    beacon = BEACONS['CEDA'] # Default
    founddc = False
    index = 0
    parts = request.path.split('/')
    while not founddc and index < len(parts):
        dc = parts[index]
        if dc not in ['ceda','badc','neodc'] and dc in DATACENTRES:
            beacon = BEACONS['EDS']
            founddc = True    
        index += 1
    context = {
        "beacon":beacon,
    }
    return context

def arrival_beacon(request):
    dc = request.path.split('/')[1] # /ceda/ -> ['','ceda','...']
    if dc not in ['ceda','badc','neodc'] and dc in DATACENTRES:
        return {"beacon":BEACONS['EDS']}
    else:
        return {"beacon":BEACONS['Arrivals']}

def account_management_urls(request):

    # Account management URLs can be overriden, otherwise defaults are used
    return {
        "account_registration_url": getattr(
            settings, "ACCOUNT_REGISTRATION_URL", ACCOUNT_REGISTRATION_URL_DEFAULT),
        "account_console_url": getattr(
            settings, "ACCOUNT_CONSOLE_URL", ACCOUNT_CONSOLE_URL_DEFAULT),
        "account_security_url": getattr(
            settings, "ACCOUNT_SECURITY_URL", ACCOUNT_SECURITY_URL_DEFAULT)
    }
