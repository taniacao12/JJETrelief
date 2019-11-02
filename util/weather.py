# interacting with openWeatherMap api

from flask import request
import urllib.request
import json
import os

DIR = os.path.dirname(__file__) or '.'
DIR += '/../'

with open(DIR + "keys/openweathermap.json", "r") as input:
    apikey = json.load(input)

key = apikey["token"]

def get_info(lat,long):
    url = "https://api.openweathermap.org/data/2.5/weather?units=imperial&appid={}&lat={}&lon={}".format(key, lat, long)
    # print(url)
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())
    # print(data)
    ret_obj = {}
    ret_obj["name"] = data["name"]
    ret_obj["conditions"] = data["weather"]
    ret_obj["curr_temp"] = data['main']['temp']
    ret_obj["low_temp"] = data["main"]["temp_min"]
    ret_obj["high_temp"] = data["main"]["temp_max"]
    ret_obj["humidity"] = data["main"]["humidity"]
    ret_obj["wdsp"] = data["wind"]["speed"]
    print(ret_obj)
    return ret_obj

# get_info(35,139)
