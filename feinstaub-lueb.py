# -*- coding: utf-8 -*-
from lxml import html
import urllib2
import csv
import config
from twython import Twython

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
        
        if (DEBUG):
            print "Fetching URL " + url
        response = urllib2.urlopen(url)
        data = response.read()
        
        dataMap[cvsFile['name']] = data
        
    return dataMap

def getLatestData( csvData ):
    "gets latest data of csv"
    
    latestValue = -1
    
    # Workaround! Find a better way to get the latest value of this CSV
    for row in csv.reader(csvData, delimiter=';'):
        #print type(row)
        if (len(row) == 1):
            latestValue = row[0]
        #latestValue = ', '.join(row)

    
    #allvalues = csv.reader(csvData, delimiter=';')
    
    #print len(allvalues)
    
    #print allvalues[1]
    
    return latestValue
    
def twitterValue( name, value ):
    "Twitters value"   

    twitter = Twython(config.APP_KEY, config.APP_SECRET, config.OAUTH_TOKEN, config.OAUTH_TOKEN_SECRET)

    twitter.update_status(status="Feinstaub in München" + name + ": " + value)
    
    
    return
    

def fetchDataAndAnounce():
    "Fetches latest PM10 data from Munich and twitters if ov threshold"    
    
    #fetchDataUrls(mainurl)
    
    dataMap = fetchData(cvsMunichFiles)
    #getLatestData(dataMap["Johanneskirchen"])
    for key in dataMap:    
        latestData = getLatestData(dataMap[key])
        
        if (int(latestData) >= pm10Threashhold):
            twitterValue(key, latestData)
        
    return
    
# Start
fetchDataAndAnounce()
    