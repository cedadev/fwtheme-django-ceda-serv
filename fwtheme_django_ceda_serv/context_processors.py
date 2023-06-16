from .default_settings import DC_TEMPLATES, DATACENTRES, BEACONS

def data_centre(request, arrivals=False):
    """
    Determine which data centre template is extended
    by browse.html
    """
    location = 'extra_data_centres/'
    data_centre_template = 'fwtheme_django/layout.html'  # default template - NERC EDS Theme

    # fwtheme_django_ceda_serv version 1.5.3

    # Dynamic Data Centre processing
    beacon = BEACONS['CEDA']
    dc = request.path.split('/')[1] # /ceda/ -> ['','ceda','...']
    if dc not in ['ceda','badc','neodc'] and dc in DATACENTRES:
        data_centre_template = location + DC_TEMPLATES[dc]
        beacon = BEACONS['EDS']
    if arrivals:
        beacon = BEACONS['Arrivals']    
    context = {
        "data_centre_template": data_centre_template,
        "data_centre": dc,
        "beacon":beacon,
    }
    return context
