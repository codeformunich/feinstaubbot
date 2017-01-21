# -*- coding: utf-8 -*-
from lxml import html

#For inspiration lxml scraping: https://github.com/okfde/odm-datenerfassung/blob/master/readdatacatalogs/bochum-scrape.py

stations = [{"name": "Lothstraße", "url": "http://aqicn.org/city/germany/bayern/munchen/lothstrasse/"},
{"name": "Stachus", "url": "http://aqicn.org/city/germany/bayern/munchen/stachus/"},
{"name": "Johanneskirchen", "url": "http://aqicn.org/city/germany/bayern/munchen/johanneskirchen/"},
{"name": "Landshuter Allee", "url": "http://aqicn.org/city/germany/bayern/munchen/landshuter-allee/"}
]

stationnr = 0

while stationnr < len(stations):
    #try:
       data = html.parse(stations[stationnr]['url'])
       print 'Trying to read ' + stations[stationnr]['url']
       stations[stationnr]['value'] = str(data.xpath("//td[@id='cur_pm10']/text()"))
       mystr = stations[stationnr]['value'] 
       print mystr.strip("[").strip("]")
       print stations[stationnr]['name'] + ': ' + str(stations[stationnr]['value'])
       stationnr += 1     
    #except:
    #   print "Try again"
