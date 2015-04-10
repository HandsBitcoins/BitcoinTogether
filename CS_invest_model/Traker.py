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

timeStamps = []
timeStamps.append(time.time())

# https://data.btcchina.com/data/ticker?market=all
params = {'market': 'all'}
parameter = urllib.urlencode(params)
             
connection = httplib.HTTPSConnection("data.btcchina.com")
connection.request("GET","/data/ticker",parameter)
response = connection.getresponse()
jsonResponse = response.read()
infoPrices = json.loads(jsonResponse)
print infoPrices
timeStamps.append(time.time())

# https://www.okcoin.com/api/ticker.do?ok=1
connection = httplib.HTTPSConnection("www.okcoin.com")
connection.request("GET","/api/ticker.do?ok=1")#, parameter)
response = connection.getresponse()
jsonResponse = response.read()
infoPrices = json.loads(jsonResponse)
print infoPrices
timeStamps.append(time.time())

# http://api.huobi.com/staticmarket/ticker_btc_json.js 
connection = httplib.HTTPSConnection("api.huobi.com")
connection.request("GET","/staticmarket/ticker_btc_json.js")
response = connection.getresponse()
jsonResponse = response.read()
infoPrices = json.loads(jsonResponse)
print infoPrices
timeStamps.append(time.time())

# https://api.bitfinex.com/v1/pubticker/:symbol
connection = httplib.HTTPSConnection("api.bitfinex.com")
connection.request("GET","/v1/pubticker/btcusd")
response = connection.getresponse()
jsonResponse = response.read()
infoPrices = json.loads(jsonResponse)
print infoPrices
timeStamps.append(time.time())

# https://www.LakeBTC.com/api_v1/ticker
connection = httplib.HTTPSConnection("www.LakeBTC.com")
connection.request("GET","/api_v1/ticker")
response = connection.getresponse()
jsonResponse = response.read()
infoPrices = json.loads(jsonResponse)
print infoPrices
timeStamps.append(time.time())

for i in range(len(timeStamps)-1):
    print timeStamps[i+1] - timeStamps[i]
    
