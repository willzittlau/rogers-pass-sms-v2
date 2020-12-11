# Import libraries
import requests
import datetime
from dateutil import tz
#keys: ['areas'], ['parkingLots']. sub keys: ['properties']: ['nameEn'], ['isOpen'], ['id'], ['parentFeatureId']
tz = tz.gettz('America/Vancouver')
date = datetime.datetime.now(tz).strftime('%Y-%m-%d')

class WRA:  
    def __init__(self, name, isOpen):
        self.name = name
        self.isOpen = isOpen

def getStatus(date):
    data=requests.get('https://www.pc.gc.ca/apps/rogers-pass/data/publish-%s' %date).json()
    # Not available:
    if data == {'error': 'not_found', 'reason': 'missing'}:
        output = 'Info for today is not available'
        return output
    # Shaughnessy
    shaughnessy = WRA(data['areas'][0]['properties']['nameEn'], data['areas'][4]['properties']['isOpen'])
    # East Rogers
    eastRogersNorth = WRA(data['areas'][1]['properties']['nameEn'], data['areas'][4]['properties']['isOpen'])
    eastRogersSouth = WRA(data['areas'][2]['properties']['nameEn'], data['areas'][4]['properties']['isOpen'])
    eastRogers = [eastRogersNorth, eastRogersSouth]
    # West Rogers
    westRogersWest = WRA(data['areas'][3]['properties']['nameEn'], data['areas'][4]['properties']['isOpen'])
    westRogersSouth = WRA(data['areas'][4]['properties']['nameEn'], data['areas'][4]['properties']['isOpen'])
    westRogersNorthEast = WRA(data['areas'][5]['properties']['nameEn'], data['areas'][4]['properties']['isOpen'])
    westRogers = [westRogersWest, westRogersSouth, westRogersNorthEast]
    # Fortitude
    fortitude = WRA(data['areas'][6]['properties']['nameEn'], data['areas'][4]['properties']['isOpen'])
    closedWRA = 'Closed WRAs: '
    openWRA = 'Open WRAs: '
    ERbool =[]
    WRbool= []
    for area in eastRogers:
        ERbool.append(area.isOpen)
    if all(ERbool) == True:
        openWRA += 'East Rogers, '
    else:
        closedWRA += 'East Rogers, '
    for area in westRogers:
        ERbool.append(area.isOpen)
    if all(ERbool) == True:
        openWRA += 'West Rogers, '
    else:
        closedWRA += 'West Rogers, '
    if fortitude.isOpen == True:
        openWRA += (fortitude.name + ', ')
    else:
        closedWRA += (fortitude.name + ', ')
    if shaughnessy.isOpen == True:
        openWRA += (shaughnessy.name + ', ')
    else:
        closedWRA += (shaughnessy.name + ', ')
    # Zones
    closedZone = 'Closed Areas: '
    openZone = 'Open Areas: '
    for area in data['areas'][7:]:
        if(area['properties']['isOpen'] == True):
            openZone += (area['properties']['nameEn'] + ', ')
        else:
            closedZone += (area['properties']['nameEn'] + ', ')
    # Parking
    closedParking = 'Closed Parking: '
    openParking = 'Open Parking: '
    for parking in data['parkingLots']:
        if parking['properties']['isOpen'] == True:
            openParking += (parking['properties']['nameEn'] + ', ')
        else:
            closedParking += (parking['properties']['nameEn'] + ', ')
    print(closedWRA)
    print(openWRA)
    print(closedZone)
    print(openZone)
    print(closedParking)
    print(openParking)

getStatus(date)