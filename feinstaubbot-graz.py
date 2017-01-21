# -*- coding: utf-8 -*-
from lxml import html
import urllib2
import csv
#import config
#from twython import Twython
import httplib, urllib
import datetime as DT

DEBUG = True

csvUrlPrefix = "http://www.umweltservice.graz.at/umweltdaten/umweltdaten.php?"

grazFiles = [
{"name": "Ost", "filename": "station=171&ort=Graz%20Ost", "row": 6},
{"name": "Nord", "filename": "station=138&ort=Graz%20Nord", "row": 10},
{"name": "West", "filename": "station=139&ort=Graz%20West", "row": 6},
{"name": "Mitte", "filename": "station=172&ort=Graz%20Mitte", "row": 8},
{"name": "Don Bosco", "filename": "station=164&ort=Graz%20Don%20Bosco", "row": 10},
{"name": "Sued", "filename": "station=170&ort=Graz%20S%FCd", "row": 12},
]

# For threshholds see http://inters.bayern.de/grenzwerte.pdf
pm10Threashhold = 50

def fetchData( cvsFiles ):
    "Fetches data from files"
    
    dataMap = {}
    
    for cvsFile in cvsFiles:
        url = csvUrlPrefix + cvsFile['filename']
        print url
        
        if (DEBUG):
            print "Fetching URL " + url
        response = urllib2.urlopen(url)
        htmldata = response.read()
        doc = html.fromstring(htmldata.decode('utf-8','ignore'))
        #parser = etree.HTMLParser(encoding='utf-8')
        
        #data = etree.parse(url, parser) 
        dataMap[cvsFile['name']] = float(doc.find('.//tr[' + str(cvsFile['row']) + ']/td[2]/table/tr[1]/td[2]/p').text.split(' ')[0]) 

    return dataMap

def twitterValue( name, value ):
    "Twitters value"   
    now = DT.datetime.now()
    #twitter = Twython(config.APP_KEY, config.APP_SECRET, config.OAUTH_TOKEN, config.OAUTH_TOKEN_SECRET)
    #twitter.update_status(status= now.strftime("%Y-%m-%d %H:%M") + " - #Feinstaub-Alarm in #Graz! PM10 bei Messstation " + name + " = " + value + "ug/m^3")

    return
    
def fetchDataAndAnounce():
    "Fetches latest PM10 data from Graz and twitters if ov threshold"    
    
    dataMap = fetchData(grazFiles)
    print dataMap
    for key in dataMap:
        print key    
        latestData = dataMap[key]
        if (int(latestData) >= pm10Threashhold):
            try:
                twitterValue(key, latestData)    
            except:
                print "Twitter error"
    return
    
if __name__ == "__main__":
    # Start
    fetchDataAndAnounce()
    
