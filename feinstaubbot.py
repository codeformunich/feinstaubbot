# -*- coding: utf-8 -*-
from lxml import html
import urllib2
import csv
import config
from twython import Twython
import httplib, urllib
import datetime as DT

# http://www.lfu.bayern.de/luft/lueb/index.htm

#For inspiration lxml scraping: https://github.com/okfde/odm-datenerfassung/blob/master/readdatacatalogs/bochum-scrape.py


DEBUG = False

csvUrlPrefix = "http://inters.bayern.de/luebmw/csv/"

cvsMunichFiles = [{"name": "Johanneskirchen", "filename": "blfu_812_PM10G.csv"},
{"name": "Landshuter Allee", "filename": "blfu_1404_PM10G.csv"},
{"name": "Lothstraße", "filename": "blfu_803_PM10G.csv"},
{"name": "Stachus", "filename": "blfu_801_PM10G.csv"}
]

mainurl = "http://inters.bayern.de/luebmw/html/aktmesswerte_lueb.php"

# For threshholds see http://inters.bayern.de/grenzwerte.pdf
pm10Threashhold = 50

# Not in use
def fetchDataUrls( fetchurl ):
    "Fetches data urls"    

    if (DEBUG):
        print "Fetching URL " + fetchurl
    data = html.parse(fetchurl)
    if (DEBUG):
        print "Fetching URL DONE"
    
    #print data.xpath("//td[text()='*Johanneskirchen*']")
    #print data.xpath("//span[@class='luebt1']/text()")
    urls = data.xpath("//a[contains(@href,'PM10.php')]/@href")
    for url in urls:
        print url
        
    return
    

def fetchData( cvsFiles ):
    "Fetches data from files"
    
    dataMap = {}
    
    for cvsFile in cvsFiles:
        url = csvUrlPrefix + cvsFile['filename']
        print url
        
        if (DEBUG):
            print "Fetching URL " + url
        response = urllib2.urlopen(url)
        data = response
        
        dataMap[cvsFile['name']] = data   
    return dataMap

def getLatestData( csvData ):
    "gets latest data of csv"
    
    # Workaround! Find a better way to get the latest value of this CSV
    for row in csv.reader(csvData, delimiter=";", lineterminator="\n"):
        latestValue = row

    return latestValue
    
def twitterValue( name, value ):
    "Twitters value"   
    now = DT.datetime.now()
    twitter = Twython(config.APP_KEY, config.APP_SECRET, config.OAUTH_TOKEN, config.OAUTH_TOKEN_SECRET)

    twitter.update_status(status= now.strftime("%Y-%m-%d %H:%M") + " - #Feinstaub-Alarm in #München! PM10 bei Messstation " + name + " = " + value + "ug/m^3")
    
    
    return
    
def saveData(fieldnames, values, timeStamp):
    "Sends values to Thingspeak"
    params = urllib.urlencode({fieldnames[0]: values[0],fieldnames[1]: values[1],fieldnames[2]: values[2],fieldnames[3]: values[3], 'key':config.THINGSPEAKKEY, 'created_at': timeStamp})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    try:
	    conn.request("POST", "/update", params, headers)
	    response = conn.getresponse()
	    #print response.status, response.reason
	    data = response.read()
	    conn.close()
    except:
        print "connection failed"

    return
    

def makeThingSpeakTimestamp(day,time):
    thetime = day + ' ' + time
    finaltime = DT.datetime.strptime(thetime, "%d.%m.%Y %H:%M").strftime("%Y-%m-%dT%H:%M:%S%z")
    finaltime = finaltime + 'GMT+0100'
    print(finaltime)
    return finaltime

def fetchDataAndAnounce():
    "Fetches latest PM10 data from Munich and twitters if ov threshold"    
    
    #fetchDataUrls(mainurl)
    
    dataMap = fetchData(cvsMunichFiles)
    #print dataMap["Johanneskirchen"]
    #print dataMap["Johanneskirchen"]
    measures = []
    TSlabels = []
    thingSpeakfields = {"Johanneskirchen":"field1","Landshuter Allee":"field2", "Lothstraße": "field3","Stachus":"field4"}
    #getLatestData(dataMap["Johanneskirchen"])
    print dataMap
    for key in dataMap:
        print key    
        latestData = getLatestData(dataMap[key])
        measures.append(latestData[2])
        TSlabels.append(thingSpeakfields[key])
        if (int(latestData[2]) >= pm10Threashhold):
            try:
                twitterValue(key, latestData[2])    
            except:
                print "Twitter error"
    print measures
    print TSlabels
    saveData(TSlabels, measures, makeThingSpeakTimestamp(latestData[0], latestData[1]))
    return
    
def aws_handler(event, context):
    fetchDataAndAnounce()

if __name__ == "__main__":
    # Start
    fetchDataAndAnounce()
    
