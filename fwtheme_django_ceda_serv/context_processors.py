from .default_settings import DC_TEMPLATES, DATACENTRES, BEACONS

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

