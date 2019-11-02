import os
import json
import urllib.request, urllib.parse

DIR = os.path.dirname(__file__) or '.'
DIR += '/../'

with open(DIR + "keys/mapquest.json", "r") as input:
    apikey = json.load(input)

KEY = apikey["token"]
geocode = "http://open.mapquestapi.com/geocoding/v1/address?key=" + KEY + "&location="

#MAPQUEST API

'''
getOptions: given a location, gives a list of all areas including that string in the form of a list of lists
Each inner list has the location information and the associated latitude and longitude
'''
def getOptions(city):
    city = urllib.parse.quote(city)
    response = urllib.request.urlopen(geocode+city)
    options = json.loads(response.read())
    results = options['results'][0]['locations']
    # print(results)
    # print(len(results))
    retlist = []
    for x in range(0, len(results)):
        alist = []
        if (results[x]['adminArea5'] != '' or results[x]['adminArea4'] != '') and results[x]['adminArea1'] == "US":
            alist.append(results[x]['adminArea5']) #city
            alist.append(results[x]['adminArea4']) #county
            alist.append(results[x]['adminArea3']) #state
            alist.append(results[x]['adminArea1']) #country
            alist.append(results[x]['latLng']['lat'])
            alist.append(results[x]['latLng']['lng'])
            retlist.append(alist)
    #print(retlist)
    return retlist

# getOptions("Brooklyn")

def getCounty(city, state):
    city = urllib.parse.quote(city)
    response = urllib.request.urlopen(geocode+city)
    options = json.loads(response.read())
    results = options['results'][0]['locations']
    for each in results:
        if each['adminArea3'] == state:
            return each['adminArea4']
    return ""

# print(getCounty("Staten Island", "NY"))
