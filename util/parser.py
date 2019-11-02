#File used to reformat tavg.json to be compatible with landing page
import os
import json

DIR = os.path.dirname(__file__) or '.'
DIR += '/../'

editted = {}
new_data = {}

with open(DIR + "data/tavgData.json", "r") as input:
    data = json.load(input)
    for year in range(1900, 2011):
        editted[year] = {}
    # for county in data.keys():
    #     new_data[county] = {}
    #     for i in range(len(data[county])):
    #         key = list(data[county][i].keys())[0]
    #         new_data[county][key] = data[county][i][key]
    for county in data.keys():
        print (county)
        no_state = county.split(",")[0]
        year = 1900
        for key in sorted(data[county].keys()):
            print(key)
            if int(key) < 2011:
                while int(key) > year:
                    editted[year][no_state] = 0
                    year += 1
                editted[year][no_state] = data[county][key]
                year += 1
        for i in range(year, 2011):
            editted[year][no_state] = 0

    # for county in data.keys():
    #     print(county)
    #     for year in range(1900, 2011):
    #         try:
    #             editted[year].append({'county':county, 'tavg': data[county][str(year)]})
    #         except:
    #             editted[year].append({'county':county, 'tavg': "0"})

#
with open(DIR + "data/newLandingData.json", 'w') as output:
    #for chunk in json.JSONEncoder().iterencode(editted):
    #    output.write(chunk)
    json.dump(editted, output)
# #
# with open(DIR + "data/tavgData.json", 'w') as output:
#     #for chunk in json.JSONEncoder().iterencode(editted):
#     #    output.write(chunk)
#     json.dump(new_data, output)
