# Import libraries
import requests
import datetime
from dateutil import tz
# keys: ['areas'], ['parkingLots']. sub keys: ['properties']: ['nameEn'], ['isOpen'], ['id'], ['parentFeatureId']
tz = tz.gettz('America/Vancouver')

class WRA:
    def __init__(self, name, isOpen, wraID):
        self.name = name
        self.isOpen = isOpen
        self.wraID = wraID

def get_status():
    from app import db
    from models import Info
    date = datetime.datetime.now(tz).strftime('%Y-%m-%d')
    data = requests.get(
        'https://www.pc.gc.ca/apps/rogers-pass/data/publish-%s' % date).json()
    # Not available:
    if data == {'error': 'not_found', 'reason': 'missing'}:
        output = 'Info for today is not available at this time. Updates usually come at 7AM, and until one has been posted all areas are CLOSED. Try again later by texting \"update\" to this number.'
        status_date = datetime.datetime.utcnow().date()
        # Append to dB
        rpdata = Info(output, status_date)
        db.session.add(rpdata)
        db.session.commit()
    else:
        # Date
        rawDate = data['validFrom']['PST'].split('T')[0]
        rawTime = data['validFrom']['PST'].split('T')[1].split('-')[0][:-3]
        statusDate = rawDate + '@' + rawTime
        titleStr = 'Status for ' + statusDate + ':'
        # Shaughnessy
        shaughnessy = WRA(data['areas'][0]['properties']['nameEn'], data['areas']
                          [0]['properties']['isOpen'], data['areas'][0]['properties']['id'])
        # East Rogers
        eastRogersNorth = WRA(data['areas'][1]['properties']['nameEn'], data['areas']
                              [1]['properties']['isOpen'], data['areas'][1]['properties']['id'])
        eastRogersSouth = WRA(data['areas'][2]['properties']['nameEn'], data['areas']
                              [2]['properties']['isOpen'], data['areas'][2]['properties']['id'])
        eastRogers = [eastRogersNorth, eastRogersSouth]
        # West Rogers
        westRogersWest = WRA(data['areas'][3]['properties']['nameEn'], data['areas']
                             [3]['properties']['isOpen'], data['areas'][3]['properties']['id'])
        westRogersSouth = WRA(data['areas'][4]['properties']['nameEn'], data['areas']
                              [4]['properties']['isOpen'], data['areas'][4]['properties']['id'])
        westRogersNorthEast = WRA(data['areas'][5]['properties']['nameEn'], data['areas']
                                  [5]['properties']['isOpen'], data['areas'][5]['properties']['id'])
        westRogers = [westRogersWest, westRogersSouth, westRogersNorthEast]
        # Fortitude
        fortitude = WRA(data['areas'][6]['properties']['nameEn'], data['areas']
                        [6]['properties']['isOpen'], data['areas'][6]['properties']['id'])
        closedWRA = 'Closed WRAs:  '
        openWRA = 'Open WRAs:  '
        ERbool = []
        WRbool = []
        for area in eastRogers:
            ERbool.append(area.isOpen)
        if all(ERbool) == True:
            openWRA += 'East Rogers, '
        else:
            closedWRA += 'East Rogers, '
        for area in westRogers:
            WRbool.append(area.isOpen)
        if all(WRbool) == True:
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
        closedZone = 'Closed Areas:  '
        openZone = 'Open Areas:  '
        for area in data['areas']:
            try:
                if (area['properties']['parentFeatureId'] == shaughnessy.wraID):
                    if shaughnessy.isOpen == True and area['properties']['isOpen'] == True:
                        openZone += (area['properties']['nameEn'] + ', ')
                    else:
                        closedZone += (area['properties']['nameEn'] + ', ')
                if (area['properties']['parentFeatureId'] == eastRogersNorth.wraID):
                    if eastRogersNorth.isOpen == True and area['properties']['isOpen'] == True:
                        openZone += (area['properties']['nameEn'] + ', ')
                    else:
                        closedZone += (area['properties']['nameEn'] + ', ')
                if (area['properties']['parentFeatureId'] == eastRogersSouth.wraID):
                    if eastRogersSouth.isOpen == True and area['properties']['isOpen'] == True:
                        openZone += (area['properties']['nameEn'] + ', ')
                    else:
                        closedZone += (area['properties']['nameEn'] + ', ')
                if (area['properties']['parentFeatureId'] == westRogersWest.wraID):
                    if westRogersWest.isOpen == True and area['properties']['isOpen'] == True:
                        openZone += (area['properties']['nameEn'] + ', ')
                    else:
                        closedZone += (area['properties']['nameEn'] + ', ')
                if (area['properties']['parentFeatureId'] == westRogersSouth.wraID):
                    if westRogersSouth.isOpen == True and area['properties']['isOpen'] == True:
                        openZone += (area['properties']['nameEn'] + ', ')
                    else:
                        closedZone += (area['properties']['nameEn'] + ', ')
                if (area['properties']['parentFeatureId'] == westRogersNorthEast.wraID):
                    if westRogersNorthEast.isOpen == True and area['properties']['isOpen'] == True:
                        openZone += (area['properties']['nameEn'] + ', ')
                    else:
                        closedZone += (area['properties']['nameEn'] + ', ')
                if (area['properties']['parentFeatureId'] == fortitude.wraID):
                    if fortitude.isOpen == True and area['properties']['isOpen'] == True:
                        openZone += (area['properties']['nameEn'] + ', ')
                    else:
                        closedZone += (area['properties']['nameEn'] + ', ')
            except:
                pass
        # Parking
        closedParking = 'Closed Parking:  '
        openParking = 'Open Parking:  '
        for parking in data['parkingLots']:
            if parking['properties']['isOpen'] == True:
                openParking += (parking['properties']['nameEn'] + ', ')
            else:
                closedParking += (parking['properties']['nameEn'] + ', ')

        # Concat and save results for dB
        status = (titleStr + '\n' + openWRA[:-2]
                    + '\n' + closedWRA[:-2] + '\n' + openZone[:-2]
                    + '\n' + closedZone[:-2] + '\n' + openParking[:-2]
                    + '\n' + closedParking[:-2])
        status_date = datetime.datetime.utcnow().date()
        # Append to dB
        rpdata = Info(status, status_date)
        db.session.add(rpdata)
        db.session.commit()


def get_status_now():
    date = datetime.datetime.now(tz).strftime('%Y-%m-%d')
    data = requests.get(
        'https://www.pc.gc.ca/apps/rogers-pass/data/publish-%s' % date).json()
    # Not available:
    if data == {'error': 'not_found', 'reason': 'missing'}:
        output = 'Info for today is not available at this time. Updates usually come at 7AM, and until one has been posted all areas are CLOSED. Try again later'
        return output
    else:
        # Date
        rawDate = data['validFrom']['PST'].split('T')[0]
        rawTime = data['validFrom']['PST'].split('T')[1].split('-')[0][:-3]
        statusDate = rawDate + '@' + rawTime
        titleStr = 'Status for ' + statusDate + ':'
        # Shaughnessy
        shaughnessy = WRA(data['areas'][0]['properties']['nameEn'], data['areas']
                          [0]['properties']['isOpen'], data['areas'][0]['properties']['id'])
        # East Rogers
        eastRogersNorth = WRA(data['areas'][1]['properties']['nameEn'], data['areas']
                              [1]['properties']['isOpen'], data['areas'][1]['properties']['id'])
        eastRogersSouth = WRA(data['areas'][2]['properties']['nameEn'], data['areas']
                              [2]['properties']['isOpen'], data['areas'][2]['properties']['id'])
        eastRogers = [eastRogersNorth, eastRogersSouth]
        # West Rogers
        westRogersWest = WRA(data['areas'][3]['properties']['nameEn'], data['areas']
                             [3]['properties']['isOpen'], data['areas'][3]['properties']['id'])
        westRogersSouth = WRA(data['areas'][4]['properties']['nameEn'], data['areas']
                              [4]['properties']['isOpen'], data['areas'][4]['properties']['id'])
        westRogersNorthEast = WRA(data['areas'][5]['properties']['nameEn'], data['areas']
                                  [5]['properties']['isOpen'], data['areas'][5]['properties']['id'])
        westRogers = [westRogersWest, westRogersSouth, westRogersNorthEast]
        # Fortitude
        fortitude = WRA(data['areas'][6]['properties']['nameEn'], data['areas']
                        [6]['properties']['isOpen'], data['areas'][6]['properties']['id'])
        closedWRA = 'Closed WRAs:  '
        openWRA = 'Open WRAs:  '
        ERbool = []
        WRbool = []
        for area in eastRogers:
            ERbool.append(area.isOpen)
        if all(ERbool) == True:
            openWRA += 'East Rogers, '
        else:
            closedWRA += 'East Rogers, '
        for area in westRogers:
            WRbool.append(area.isOpen)
        if all(WRbool) == True:
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
        closedZone = 'Special Closures:  '
        for area in data['areas']:
            # Logic check: parent is open & area is closed = special closure
            try:
                if (area['properties']['parentFeatureId'] == shaughnessy.wraID):
                    if shaughnessy.isOpen == True and area['properties']['isOpen'] == False:
                        closedZone += (area['properties']['nameEn'] + ', ')
                if (area['properties']['parentFeatureId'] == eastRogersNorth.wraID):
                    if eastRogersNorth.isOpen == True and area['properties']['isOpen'] == False:
                        closedZone += (area['properties']['nameEn'] + ', ')
                if (area['properties']['parentFeatureId'] == eastRogersSouth.wraID):
                    if eastRogersSouth.isOpen == True and area['properties']['isOpen'] == False:
                        closedZone += (area['properties']['nameEn'] + ', ')
                if (area['properties']['parentFeatureId'] == westRogersWest.wraID):
                    if westRogersWest.isOpen == True and area['properties']['isOpen'] == False:
                        closedZone += (area['properties']['nameEn'] + ', ')
                if (area['properties']['parentFeatureId'] == westRogersSouth.wraID):
                    if westRogersSouth.isOpen == True and area['properties']['isOpen'] == False:
                        closedZone += (area['properties']['nameEn'] + ', ')
                if (area['properties']['parentFeatureId'] == westRogersNorthEast.wraID):
                    if westRogersNorthEast.isOpen == True and area['properties']['isOpen'] == False:
                        closedZone += (area['properties']['nameEn'] + ', ')
                if (area['properties']['parentFeatureId'] == fortitude.wraID):
                    if fortitude.isOpen == True and area['properties']['isOpen'] == False:
                        closedZone += (area['properties']['nameEn'] + ', ')
            except:
                pass
        # Add special Closure to start of message
        if closedZone != 'Special Closures:  ':
            closedZone = closedZone[:-2] + ' - Please check Parks Canada for more details!'
            titleStr += + '\n' + closedZone
        # Parking
        closedParking = 'Closed Parking:  '
        openParking = 'Open Parking:  '
        for parking in data['parkingLots']:
            if parking['properties']['isOpen'] == True:
                openParking += (parking['properties']['nameEn'] + ', ')
            else:
                closedParking += (parking['properties']['nameEn'] + ', ')
        # Concat and save results for dB
        status = (titleStr
                    + '\n' + '\n' + openWRA[:-2]
                    + '\n' + '\n' + closedWRA[:-2] 
                    + '\n' + '\n' + openParking[:-2]
                    + '\n' + '\n' + closedParking[:-2])
        return status