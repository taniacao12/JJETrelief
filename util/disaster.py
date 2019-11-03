import os

import json
import urllib.request

DIR = os.path.dirname(__file__) or '.'
DIR += '/../'

#===============================================================================
# COUNTY/CITY WEATHER INFORMATION FOR SEARCH FUNCTION
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

# def getcityid(city, state):
#     print("getting city id for", city)
#     with open (DIR + "data/city.json", "r") as cities:
#         city_list = json.load(cities)
#         for key in city_list.keys():
#             if city in key and state in key:
#                 return city_list[key]
#     return "NOT FOUND"
# #
# # print(getcityid("Salt Lake City", "UT"))
# # print(getcityid("Brooklyn", "NY"))
#
# def getcountylist():
#     offset = 0
#     ret_dict = {}
#     for x in range(0, 4):#total: 3,179 counties
#         url = "http://www.ncdc.noaa.gov/cdo-web/api/v2/locations?locationcategoryid=CNTY&limit=1000&offset=" + str(offset)
#         req = urllib.request.Request(url, data=None, headers=token)
#         response = urllib.request.urlopen(req)
#         data = json.loads(response.read())
#         for each in data['results']:
#             ret_dict[each['name']] = each['id']
#         offset += 1000
#     return ret_dict
#
# # county_list = getcountylist()
# # print(len(county_list))
# #
# # with open("county.json", 'w') as outfile:
# #     json.dump(county_list, outfile)
#
# def getcountyid(county, state):
#     print("getting county id for", county)
#     with open (DIR + "data/county.json", "r") as counties:
#         county_list = json.load(counties)
#         for key in county_list.keys():
#             if county in key and state in key:
#                 return county_list[key]
#     return "NOT FOUND"
#
# # print(getcountyid("Kings County", "NY"))
#
# def getstatelist():
#     for x in range(0,2):#total: 1988 cities
#         url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/locations?locationcategoryid=ST&limit=51"
#         req = urllib.request.Request(url, data=None, headers=token)
#         response = urllib.request.urlopen(req)
#         data = json.loads(response.read())
#     # print(data)
#     data = data['results']
#     del data[8] # remove District of Columbia
#     ret_dict = {}
#     for each in data:
#         ret_dict[codes[each['name']]] = each['id']
#     return ret_dict
#
# # state_list = getstatelist()
# # print(state_list)
#
# # with open("state.json", 'w') as outfile:
# #     json.dump(state_list, outfile)
#
# def getstateid(state):
#     print("getting state id for", state)
#     with open (DIR + "data/state.json", "r") as states:
#         state_list = json.load(states)
#         for key in state_list.keys():
#             if state == key:
#                 return state_list[key]
#     return "NOT FOUND"
#
# print(getstateid("FL"))
#
# def getTemp(id, city, county, state):
#     ID = id
#     stations = ""
#     url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/stations?datatypeid=TAVG&locationid=" + ID
#     req = urllib.request.Request(url, data=None, headers=token)
#     response = urllib.request.urlopen(req)
#     data = json.loads(response.read())
#     for i in range(0, len(data['results'])):
#         s = data['results'][i]['id']
#         #remove the colon and everything before it
#         s = s.split(':', 1)[-1]
#         stations += s + ","
#     #remove trailing comma
#     stations = stations[:-1]
#     # print(stations)
#     url = "https://www.ncei.noaa.gov/access/services/data/v1?dataset=global-summary-of-the-year&dataTypes=TAVG&stations=" + stations + "&startDate=1900-01-01&endDate=2018-12-31&format=json&units=standard"
#     req = urllib.request.Request(url, data=None, headers=token)
#     response = urllib.request.urlopen(req)
#     data = json.loads(response.read())
#     ret_data = []
#     for entry in data:
#         if 'TAVG' in entry:
#             ret_data.append({'DATE': entry['DATE'], 'TAVG': entry['TAVG']})
#     return ret_data
#
# def getPrecip(id, city, county, state):
#     ID = id
#     stations = ""
#     url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/stations?datatypeid=PRCP&locationid=" + ID
#     req = urllib.request.Request(url, data=None, headers=token)
#     response = urllib.request.urlopen(req)
#     data = json.loads(response.read())
#     for i in range(0, len(data['results'])):
#         s = data['results'][i]['id']
#         s = s.split(':', 1)[-1]
#         stations += s + ","
#     stations = stations[:-1]
#     # print(stations)
#     url = "https://www.ncei.noaa.gov/access/services/data/v1?dataset=global-summary-of-the-year&dataTypes=PRCP&stations=" + stations + "&startDate=1900-01-01&endDate=2018-12-31&format=json&units=standard"
#     req = urllib.request.Request(url, data=None, headers=token)
#     response = urllib.request.urlopen(req)
#     data = json.loads(response.read())
#     # print(data)
#     ret_data = []
#     for entry in data:
#         if 'PRCP' in entry:
#             ret_data.append({'DATE': entry['DATE'], 'PRCP': entry['PRCP']})
#     return ret_data
#
# def getSearchInfo(city, county, state):
#     ID = "NOT FOUND"
#     if city != "":
#         ID = getcityid(city, state)
#     if ID == "NOT FOUND" and county != "":
#         ID = getcountyid(county, state)
#     if ID == "NOT FOUND":
#         ID = getstateid(state)
#     temp_data = getTemp(ID, city, county, state)
#     precip_data = getPrecip(ID, city, county, state)
#     return temp_data, precip_data
#
# # print(getSearchInfo("", "Kings County", "NY"))
