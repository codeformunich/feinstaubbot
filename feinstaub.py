# -*- coding: utf-8 -*-
from lxml import html

#For inspiration lxml scraping: https://github.com/okfde/odm-datenerfassung/blob/master/readdatacatalogs/bochum-scrape.py

stations = [{"name": "Lothstraße", "url": "http://aqicn.org/city/germany/bayern/munchen/lothstrasse/"},
{"name": "Stachus", "url": "http://aqicn.org/city/germany/bayern/munchen/stachus/"},
{"name": "Johanneskirchen", "url": "http://aqicn.org/city/germany/bayern/munchen/johanneskirchen/"},
{"name": "Landshuter Allee", "url": "http://aqicn.org/city/germany/bayern/munchen/landshuter-allee/"}
]

for station in stations:
    data = html.parse(station['url'])
    print data.xpath("//td[@id='cur_pm10']/text()")[0]
