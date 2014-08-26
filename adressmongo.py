#GOAL  - open a file of addressess, read each line, remove tabs, create a 2-d array of [lat,long]
#and enter the result in a MongoDB collection

import sys
import pymongo #must import for constants ASCENDING and DESCENDING
from datetime import datetime
from pymongo import Connection
from pymongo.errors import ConnectionFailure
from pymongo.errors import PyMongoError
from pygeocoder import Geocoder
from pygeocoder import GeocoderError
def main():
  
    try:
        c = Connection(host="localhost", port=27017)
        print "Connected to MongoDB"
    except ConnectionFailure as e:
        sys.stderr.write("Could not connect to MongoDB: %s" % e)
        sys.exit(1)
    dbh = c["mydb"]
    assert dbh.connection == c
    

    makeGeoObjectFromFile("addressFile.txt",dbh)
    
    
def makeGeoObjectFromFile(filename,dbh):  
    file = open(filename)
    counter=0
    for line in file:
       
        line= line.replace("\t"," ").replace("\"","").replace("\n","")
       #print line
        user = makeGeoObjectFromLine(line,"username","user_location")
        print user
    
        dbh.usersgeo3.insert(user, safe=True)
        print "Successfully inserted document: %s" % user
       
    
    
def makeGeoObjectFromLine(address,address_key,location_key):
   
    try:
        origin = Geocoder.geocode(address)
        x1 = origin[0].coordinates[1] #reversed
        y1 = origin[0].coordinates[0] #reversed
    except GeocoderError as e:
        x1=0
        y1=0
        
        print "BAD ADDRESS"
        print address
        print e
   
    user_1 ={address_key:address, location_key:[x1,y1]} 
       
    return user_1

#PLACE CODE HERE
if __name__ == "__main__":
    main()