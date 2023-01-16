"""
Default settings for this app
"""

__author__ = "William Tucker"
__copyright__ = "Copyright 2018 UK Science and Technology Facilities Council"

# NERC Datacentres
DATACENTRES = {
    'ceda': 'Centre for Environmental Data Analysis',
    'badc': 'Centre for Environmental Data Analysis',
    'neodc': 'Centre for Environmental Data Analysis',
    'pdc': 'British Antarctic Survey',
    'bodc': 'British Oceanographic Data Centre',
    'eidc': 'Environmental Information Data Centre',
    'ngdc': 'British Geological Survey',
    'ssdc': 'UK Solar System Data Centre',
    'edc' : 'UK Energy Research Centre',
    'sparc': 'Stratosphere-troposphere Processes And their Role in Climate'
}
# DATACENTRE THEMES
DC_TEMPLATES = {
    'ceda':'',
    'badc': '',
    'neodc': '',
    'pdc': 'pdc.html',
    'bodc': 'bodc.html',
    'eidc': 'eidc.html',
    'ngdc': 'ngdc.html',
    'ssdc': 'ssdc.html',
    'edc': 'edc.html',
    'sparc': 'sparc.html'
}

# Enable the user_status block for Django-authenticated users
USE_DJANGO_USER_STATUS = False

# Enable the user_status block for CEDA-authenticated users
USE_CEDA_USER_STATUS = True
