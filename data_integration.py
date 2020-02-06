import parser
import os
import re
import string
from petl import *

# data load 
fire_station = fromcsv("data/Fire-Stations.xls")
station_regions = fromcsv("data/Station-Regions.xls")
station_locations = fromxml("data/Station-Locations.xml","STATION",{"Name":"NAME","Longitude":"LONG","Latitude":"LAT"})

#1.1 Remove unreadable characters
pattern = re.compile(r'[^\x00-\x7F]')
pattern.sub("",fire_station[1][1])
for col in header(fire_station):
    fire_station = convert(fire_station, col, lambda x: pattern.sub("",x))
fire_station

#Task 1.2 Create Email 
fire_station = addfield(fire_station, "Email", lambda x: re.sub(r'\s+','',x['Fire Station'].lower())+"@mail.com")

#Task 1.3 Merge Data
intermediate_table = annex(fire_station, station_locations)
intermediate_table = leftjoin(intermediate_table, station_regions, lkey="Region",rkey="Region Code")
fire_station_locations =cut(intermediate_table, 'RegionID','Stn Number','Fire Station','Stn Type','Address','Phone Number','Fax Number','Email','Latitude','Longitude')

#Task 1.4-1.5 CorrectField Names and order
fire_station_locations = rename(fire_station_locations,{'Stn Number':'Station Number','Fire Station':'Station Name','Stn Type':'Station Type','Address':'Street Address','Email':'E-Mail','Latitude':'Lat','Longitude':'Lon'})

#Task 1.6
fire_station_locations = sort(fire_station_locations,["RegionID","Station Number"])

# saving to a file
tocsv(fire_station_locations,"Fire_Station_Locations")
