__author__ = 'Ray'

from TwitterSearch import *
from geopy import geocoders
import arcpy
from arcpy import env

env.workspace = "C:\Users\Ray\Desktop\School\python\Lab7"
arcpy.env.overwriteOutput = True

#spref = 3857
#spat = arcpy.SpatialReference("WGS 1984 UTM Zone 11N")
arcpy.CreateFeatureclass_management("C:\Users\Ray\Desktop\School\python\Lab7", "Snow", "POINT","","","", "WGS 1984 UTM Zone 11N")

fc = ("Snow.shp")
arcpy.AddField_management(fc, "NAME", "TEXT", "", "", 20, "", "NULLABLE")
arcpy.AddField_management(fc, "TWEETED", "TEXT", "", "", 150, "", "NULLABLE")
arcpy.AddField_management(fc, "SCRN_NAM", "TEXT", "", "", 20, "", "NULLABLE")
arcpy.AddField_management(fc, "LAT", "FLOAT", "", "", 20, "", "NULLABLE")
arcpy.AddField_management(fc, "LONG", "FLOAT", "", "", 20, "", "NULLABLE")
arcpy.AddField_management(fc, "DATE", "TEXT", "", "", 30, "", "NULLABLE")

curs1 = arcpy.da.InsertCursor("C:\Users\Ray\Desktop\School\python\Lab7/Snow.shp", ["SHAPE@XY"])

def geo(location):
    g = geocoders.GoogleV3()
    loc = g.geocode(location)
    return loc.latitude, loc.longitude


try:
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(["snow"]) # let's define all words we would like to have a look for
    tso.set_include_entities(False) # and don't give us all those entity information
    tso.set_geocode(42.9047,-78.8494 ,500,False)
    #object creation with secret token
    ts = TwitterSearch(
        consumer_key = 'lFYhtByukAE7OUZ0FAXPfD6UC',
        consumer_secret = 'iOkrbMM6iG8S0cWIGeEE33vLyxMtYWPNdjL4XXesuBKzCWDnyq',
        access_token = '2865035572-xIeTvxAlKZc3m8dA87rNjwlIuArQ3V9fbuwBWqT',
        access_token_secret = '4cNQjgnOYUs1YUjjiHj5g868g7iyjOHu0gcpRVhAmgzcx'
     )

    Points = []     # this is where the fun actually starts :)
    for tweet in ts.search_tweets_iterable(tso):

        if tweet["place"] is not None:
            curs2 = arcpy.da.UpdateCursor("C:\Users\Ray\Desktop\School\python\Lab7/Snow.shp",
                                      ["NAME", "TWEETED", "SCRN_NAM", "LAT", "LONG", "DATE"])

            T = (tweet['coordinates'])
            H = list(reduce(lambda x, y: x + y, T.items()))
            L = H[3]
            V = []
            U = L[1], L[0]
            x = L[1]
            y = L[0]
            V.append(U)
            curs1.insertRow(V)
            name = (tweet['user']['name'])
            text = (tweet['text'])
            SN = (tweet['user']['screen_name'])
            Time = (tweet['created_at'])

            for row in curs2:
                if row[0] == " ":
                    row[0] = name
                    curs2.updateRow(row)
                elif row[1] == " ":
                    row[1] = text
                    curs2.updateRow(row)
                elif row[2] == " ":
                    row[2] = SN
                    curs2.updateRow(row)
                elif row[3] == 0:
                    row[3] = x
                    curs2.updateRow(row)
                elif row[4] == 0:
                    row[4] = y
                    curs2.updateRow(row)
                elif row[5] == " ":
                    row[5] = Time
                    curs2.updateRow(row)


            print x, y


            print( "@%s tweeted: %s" % (tweet["user"]["screen_name"], tweet["text"]))
            (lat, lng) = geo(tweet["place"]["full_name"])
            Points.append(arcpy.Point(lat, lng))
            print "(" + str(lat) +", " +str(lng)+")"



except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)