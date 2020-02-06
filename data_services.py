from petl import *
from bottle import route, run,template,debug, response
import json
import os

#query directory creation
if('query' not in os.listdir()):
    os.mkdir('query')
#data load
fire_station_locations = fromcsv("Fire_station_locations")
station_regions = fromcsv("data/Station-Regions.xls")

#service helpers 
def JsonAccording2Region(x,file):
    if(x==0):
        tab = fire_station_locations
    else:
        tab = select(fire_station_locations,'RegionID',lambda rec: rec == str(x))
    tab = cut(tab, 'Station Number', 'Station Name', 'Street Address', 'Phone Number', 'E-Mail', 'Lat', 'Lon')
    return returnJson(tab, file)
    
def returnJson(table,file):
    tojson(table, file)
    with open(file) as f:
        data = json.load(f)
    return json.dumps(data)

filepath = 'query/'

#route
@route('/getstations/regionid/<regionid:int>')
def getStations(regionid):
    query = str(regionid)+'.json'
    file = filepath+query
    data = JsonAccording2Region(regionid, file)
    response.content_type = 'application/json'
    return data

@route('/getregions')
def getRegions():
    query='regions.json'
    file = filepath+query
    tab= cut(station_regions,'RegionID','Region Name')
    return returnJson(tab, file)


debug(True)
run(host='localhost', port=8080)