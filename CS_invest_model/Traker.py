import httplib
import urllib       
import json
import time
import math
import random

import tweepy

# btcchina
# okcoin
# huobi
# bitfinex
# lakebtc

def getPriceBtcChina():
    # https://data.btcchina.com/data/ticker?market=all
    params = {'market': 'all'}
    parameter = urllib.urlencode(params)
                 
    connection = httplib.HTTPSConnection("data.btcchina.com")
    connection.request("GET","/data/ticker",parameter)
    response = connection.getresponse()
    jsonResponse = response.read()
    infoPrices = json.loads(jsonResponse)
    
    return infoPrices

def getPriceOkcoin():
    # https://www.okcoin.com/api/ticker.do?ok=1
    connection = httplib.HTTPSConnection("www.okcoin.com")
    connection.request("GET","/api/ticker.do?ok=1")#, parameter)
    response = connection.getresponse()
    jsonResponse = response.read()
    infoPrices = json.loads(jsonResponse)

    return infoPrices

def getPriceHuobi():
    # http://api.huobi.com/staticmarket/ticker_btc_json.js 
    connection = httplib.HTTPSConnection("api.huobi.com")
    connection.request("GET","/staticmarket/ticker_btc_json.js")
    response = connection.getresponse()
    jsonResponse = response.read()
    infoPrices = json.loads(jsonResponse)
    
    return infoPrices

def getPriceBitfinex():
    # https://api.bitfinex.com/v1/pubticker/:symbol
    connection = httplib.HTTPSConnection("api.bitfinex.com")
    connection.request("GET","/v1/pubticker/btcusd")
    response = connection.getresponse()
    jsonResponse = response.read()
    infoPrices = json.loads(jsonResponse)
    
    return infoPrices

def getPriceLakeBTC():
    # https://www.LakeBTC.com/api_v1/ticker
    connection = httplib.HTTPSConnection("www.LakeBTC.com")
    connection.request("GET","/api_v1/ticker")
    response = connection.getresponse()
    jsonResponse = response.read()
    infoPrices = json.loads(jsonResponse)

    return infoPrices

def testTimeCaculation():
    fileOpened = open("./72000test.csv",'r')
    newList = fileOpened.readlines()
    fileOpened.close()
    
    dataList = []
    for eachLine in newList:
        dataList.append(float(eachLine))
     
    import numpy
    timeStamps = []    
    timeStamps.append(time.time())
    print numpy.std(dataList)
    timeStamps.append(time.time())
    print numpy.mean(dataList)
    timeStamps.append(time.time())
     
    print len(dataList)
    for i in range(len(timeStamps)-1):
        print timeStamps[i+1] - timeStamps[i]
    print timeStamps[-1] - timeStamps[0]
    
def testGetPrice():
    dataPrice = []
    
    timeStamps = []    
    timeStamps.append(time.time())
    dataPrice.append(getPriceBtcChina())
    timeStamps.append(time.time())
    dataPrice.append(getPriceOkcoin())
    timeStamps.append(time.time())
    dataPrice.append(getPriceHuobi())
    timeStamps.append(time.time())
    dataPrice.append(getPriceBitfinex())
    timeStamps.append(time.time())
    dataPrice.append(getPriceLakeBTC())
    timeStamps.append(time.time())
     
    for i in range(len(timeStamps)-1):
        print timeStamps[i+1] - timeStamps[i]
    print timeStamps[-1] - timeStamps[0]
        
    print dataPrice[0]['ticker']['sell']
    print dataPrice[0]['ticker']['buy']
    print dataPrice[1]['ticker']['sell']
    print dataPrice[1]['ticker']['buy']
    print dataPrice[2]['ticker']['sell']
    print dataPrice[2]['ticker']['buy']
    print dataPrice[3]['bid']
    print dataPrice[3]['ask']
    print dataPrice[4]['USD']['bid']
    print dataPrice[4]['USD']['ask']

def testTweepy():
    auth = tweepy.OAuthHandler("","")
    auth.set_access_token("", "")
    
    api = tweepy.API(auth)
    
    api.send_direct_message(user = "lesenic", text = "TEST")

def testEmail():
    import smtplib
    import email
    
    msg = email.mime.Text.MIMEText("This is test message")

    addrEmail = "rectifying@gmail.com"

    msg['Subject'] = "Bitcoin alter message test"
    msg['From'] = addrEmail
    msg['To'] = addrEmail
    
    s = smtplib.SMTP('smtp.gmail.com:587')
    s.ehlo()
    s.starttls()
    s.login("rectifying@gmail.com", "")
    s.sendmail(addrEmail, [addrEmail], msg.as_string())
    s.close()

# testGetPrice()
# testTweepy()
testEmail()
    