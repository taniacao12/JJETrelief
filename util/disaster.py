import os

import json
import urllib.request

DIR = os.path.dirname(__file__) or '.'
DIR += '/../'

#===============================================================================
# EARTHQUAKE INFORMATION FOR SEARCH FUNCTION
#===============================================================================

def getDate(start, end):
    '''Return a dictionary of available cities in the format of "city":"id".'''
    ret_dict = {}
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=" + str(start) + "&endtime=" + str(end)
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())
    for each in data['features']:
        ret_dict[each['properties']['title']] = each['properties']['mag']
    return ret_dict
