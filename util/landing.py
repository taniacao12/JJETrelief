import json
import urllib.request
import time
import os

DIR = os.path.dirname(__file__) or '.'
DIR += '/../'

with open(DIR + "keys/climatedataonline.json", "r") as input:
    token = json.load(input)

#===============================================================================
# COUNTY WEATHER INFORMATION FOR LANDING PAGE
#===============================================================================
def getCountyID():
    '''
    returns a dictionary
    keys: name of county
    value: county id
    '''
    cntyIDs = []
    offset = 0
    for x in range(0, 4):#total: 3,179 counties
        url = "http://www.ncdc.noaa.gov/cdo-web/api/v2/locations?locationcategoryid=CNTY&limit=1000&offset=" + str(offset)
        req = urllib.request.Request(url, data=None, headers=token)
        response = urllib.request.urlopen(req)
        data = json.loads(response.read())
        print(len(data['results']))
        for i in range(0, len(data['results'])):
            cntyIDs.append([data['results'][i]['name'], data['results'][i]['id']])
        offset += 1000
    with open('cntyIDs.json', 'w') as outfile:
        json.dump(cntyIDs, outfile)

#getCountyID()

def getStations(lbound, ubound):
    info = []
    with open('cntyIDs.json') as json_file:
        cntyIDs = json.load(json_file)
    if ubound == 4000:
        ubound = len(cntyIDs)
    print(ubound)
    for x in range(lbound, ubound):
        print(x)
        #get the stations
        stations = ""
        url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/stations?datatypeid=TAVG&locationid=" +cntyIDs[x][1]
        req = urllib.request.Request(url, data=None, headers=token)
        response = urllib.request.urlopen(req)
        data = json.loads(response.read())
        if 'results' in data:
            for i in range(0, len(data['results'])):
                s = data['results'][i]['id']
                #remove the colon and everything before it
                s = s.split(':', 1)[-1]
                stations += s + ","
            #remove trailing comma
            stations = stations[:-1]
            info.append([cntyIDs[x][0],stations])
            time.sleep(1)
    with open('stations.json', 'a') as stationfile:
        json.dump(info, stationfile)

#getStations(0, 1000) ALREADY RAN THIS
#getStations(1000, 2000) ALREADY RAN THIS
#getStations(2000, 3000) ALREADY RAN THIS
#getStations(3000, 4000) ALREADY RAN THIS


def getCntyInfo(batch):
    with open('stations.json') as json_file:
        stations = json.load(json_file)
    info = {}
    with open('tavg.json') as f:
        d = json.load(f)
    for x in range(0, len(stations[batch])):
        #get the info
        url = "https://www.ncei.noaa.gov/access/services/data/v1?dataset=global-summary-of-the-year&dataTypes=TAVG&stations=" + stations[batch][x][1] + "&startDate=1900-01-01&endDate=2018-12-31&format=json&units=standard"
        req = urllib.request.Request(url, data=None, headers=token)
        response = urllib.request.urlopen(req)
        data = json.loads(response.read())
        alist = []
        for j in range(0, len(data)):
            if 'TAVG' in data[j]:
                alist.append({data[j]['DATE']:data[j]['TAVG']})
            else:
                alist.append({data[j]['DATE']: ""})
        print(stations[batch][x][0])
        d.update({stations[batch][x][0]: alist})
    with open('tavg.json', 'w') as outfile:
        json.dump(d, outfile)

#getCntyInfo(0)
#getCntyInfo(1)
#getCntyInfo(2)
#getCntyInfo(3)
