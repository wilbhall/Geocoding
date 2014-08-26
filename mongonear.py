from datetime import datetime
from pymongo import Connection
from pymongo.errors import ConnectionFailure

def main():
    try:
        c = Connection(host="localhost", port=27017)
        print "Connected to MongoDB"
    except ConnectionFailure, e:
        sys.stderr.write("Could not connect to MongoDB: %s" % e)
        sys.exit(1)
    dbh = c["mydb"]
    assert dbh.connection == c
 

    earth_radius_km = 6371.0
    max_distance_km = 5.0
    max_distance_radians = max_distance_km / earth_radius_km
    lat=40
    long = -70
    nearest_users = dbh.usersgeo3.find(
        {"user_location":
            {"$nearSphere":[long,lat],
             "$maxDistance":max_distance_radians
              }
        }
    ).limit(16)
    #print the users
    for user in nearest_users:
        #assume user_location property is array [x,y]
        print "User %s is at location %s,%s\n" %(user["username"],
                                               user["user_location"][0],user["user_location"][1]
                                               )
    

if __name__ == "__main__":
    main()