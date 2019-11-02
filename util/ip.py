# interacting with ipstack api
from flask import request
import urllib.request
import json
import os

DIR = os.path.dirname(__file__) or '.'
DIR += '/../'

with open(DIR + "keys/ipstack.json", "r") as input:
    apikey = json.load(input)

KEY = apikey["token"]

def get_coord():
    IP = request.remote_addr
    if IP == "127.0.0.1": # if running on local host
        req = urllib.request.Request("https://api.ipify.org?format=json")
        IP = json.loads(urllib.request.urlopen(req).read())['ip']
    # print(IP)
    URL = "http://api.ipstack.com/" + IP +"?access_key=" + KEY + "&output=json"
    req = urllib.request.Request(URL)
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())
    return data
