import httplib
import urllib       
import json
import time
import math
import random

# btcchina
# okcoin
# huobi
# bitfinex
# lakebtc

# https://data.btcchina.com/data/ticker?market=all
params = {'market': 'all'}
parameter = urllib.urlencode(params)

#GET https://api.korbit.co.kr/v1/ticker/detailed                
connection = httplib.HTTPSConnection("data.btcchina.com")
connection.request("GET","/data/ticker",parameter)
response = connection.getresponse()
jsonResponse = response.read()
infoPrices = json.loads(jsonResponse)
print infoPrices

# https://www.okcoin.com/api/klineData.do?marketFrom=34&type=2&limit=1000&coinVol=1
# https://www.okcoin.com/api/klineData.do?marketFrom=34&type=2&since=1428623100000&coinVol=1
# https://www.okcoin.com/api/klineData.do?marketFrom=34&type=2&since=1428624000000&coinVol=1
# flooredTiem = math.floor(time.time()/100)*100000
# strTime = "%012d" % flooredTiem 
# print strTime
# #1428623100000
# #1428624281000
# #1428624000000
# params = {'marketFrom': '34',
#           'type': '2',
#           'since': strTime,
#           'coinVol': '1'}
# parameter = urllib.urlencode(params)
# 
# connection = httplib.HTTPSConnection("www.okcoin.com")
# connection.request("GET","/api/klineData.do",parameter)
# response = connection.getresponse()
# infoPrices = response.read()
# print infoPrices

# https://api.huobi.com/staticmarket/td_btc.html?0.7971218014135957
connection = httplib.HTTPSConnection("api.huobi.com")
connection.request("GET","/staticmarket/td_btc.html",str(random.random()))
response = connection.getresponse()
infoPrices = response.read()

print infoPrices


