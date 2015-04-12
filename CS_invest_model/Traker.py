import httplib
import urllib
import json
import time
import math
import random

import ChiperSimple
# btcchina
# okcoin
# huobi
# bitfinex
# lakebtc


class TrakerBitcoinBollinger(object):
    def __init__(self):
        pass
    
    def initTraker(self):
        # 1sec interval, 5days
        self.numDataPrice = 5*24*60*60 
        
        self.counter = 0
        self.bids = [0.0 for _ in range(self.numDataPrice)]
        self.asks = [0.0 for _ in range(self.numDataPrice)]
        
        self.menuMarket = {0: self.getPriceBtcChina, 
                           1: self.getPriceOkcoin, 
                           2: self.getPriceHuobi, 
                           3: self.getPriceBitfinex, 
                           4: self.getPriceLakeBTC}
        
        self.menuTrading = {0: self.bids,
                            1: self.asks}
        
        self.menuStrTrading = {0: "Bid",
                               1: "Ask"}
            
        self.timeBeacon = 1.0
        self.timeMailBeacon = 600/int(self.timeBeacon)
        
        self.dictTendency = {'upper': 0,
                             'normal': 1,
                             'lower': 2}
        self.tendency = self.dictTendency['normal']
        
        self.counterMail = 0
        
    def setMailServer(self):
        import EmailSMTPAlter
        
        self.mailServer = EmailSMTPAlter.SMTPEmailAlter()
        self.mailServer.initEmail()
                
            
    def activateTraker(self,market=0):
        import msvcrt
        
        self.setMailServer()
        
        while True:
            dataPrice = self.menuMarket[market]()
            timeBeforeCheck = time.time()
            
            numStdDevi = []
            numMean = []
            
            self.counter += 1
            if self.counter > self.numDataPrice:
                self.counter = self.numDataPrice
            else:
                print "Step Counter:", str(self.counter)
                print "Data Percent:", str(float(self.counter)/float(self.numDataPrice)*100.0), "%"
                print
                
            for i in range(2):
                self.menuTrading[i].insert(0,float(dataPrice[i]))
                self.menuTrading[i].pop()                            
                numStdDevi.append(self.getStandardDeviation(i))
                numMean.append(self.getMeanMoving(i))

            for i in range(2):
                print self.menuStrTrading[i], "price |   Mean  |    Std    |   Upper   |  Lower"
                upperBound = numMean[i]+2*numStdDevi[i]
                lowerBound = numMean[i]-2*numStdDevi[i]
                print ' {0:4.2f}    {1:4.2f}    {2:-0.5f}     {3:4.2f}    {4:4.2f}'.format(float(dataPrice[i]), numMean[i], numStdDevi[i], upperBound, lowerBound)
                
            self.checkOutOfBox(dataPrice[1],upperBound,lowerBound)
                
            timeSleep = self.timeBeacon - (time.time() - timeBeforeCheck)
            
            if timeSleep < 0.0:
                timeSleep = 0.0
            
            print 
            print "Process Time: " + str(self.timeBeacon-timeSleep)
            print "  Sleep Time: " + str(timeSleep)
            print 
            
            time.sleep(timeSleep)

    def checkOutOfBox(self,price,upper,lower):
        #5 hours data
        if self.counter > 21600/int(self.timeBeacon):
            alterState = True
            subject = ""
            content = "Price: " + str(price)
            
            if price > upper:
                subject = "^^^ Bitcoin price is over upper bound ^^^"                
                self.tendency = self.dictTendency['upper']                
            elif lower > price:
                subject = "VVV Bitcoin price is under lower bound VVV"                                
                self.tendency = self.dictTendency['lower']
            else:
                alterState = False
                self.tendency = self.dictTendency['normal']
                
            if self.counterMail == 0 and alterState:
                self.counterMail = self.timeMailBeacon
                self.mailServer.sendEmail(subject,content)
                
            if not alterState:
                self.counterMail = 0
            else:
                self.counterMail -= 1
                 
            return alterState        
        return False

    def getStandardDeviation(self,menu=0):
        import numpy
        arrData = self.menuTrading[menu]
        
        if self.counter > len(arrData):
            return numpy.std(arrData)
        else:
            return numpy.std(arrData[0:self.counter])        

    def getMeanMoving(self,menu=0):
        import numpy
        arrData = self.menuTrading[menu]
        
        if self.counter > len(arrData):
            return numpy.mean(arrData)
        else:
            return numpy.mean(arrData[0:self.counter])
        
    def getPriceBtcChina(self):
        # https://data.btcchina.com/data/ticker?market=all
        params = {'market': 'all'}
        parameter = urllib.urlencode(params)
                     
        connection = httplib.HTTPSConnection("data.btcchina.com")
        connection.request("GET","/data/ticker",parameter)
        response = connection.getresponse()
        jsonResponse = response.read()
        infoPrices = json.loads(jsonResponse)
        
        priceBid = infoPrices['ticker']['buy']
        priceAsk = infoPrices['ticker']['sell']
        
        return [priceBid,priceAsk]
    
    def getPriceOkcoin(self):
        # https://www.okcoin.com/api/ticker.do?ok=1
        connection = httplib.HTTPSConnection("www.okcoin.com")
        connection.request("GET","/api/ticker.do?ok=1")#, parameter)
        response = connection.getresponse()
        jsonResponse = response.read()
        infoPrices = json.loads(jsonResponse)
    
        priceBid = infoPrices['ticker']['buy']
        priceAsk = infoPrices['ticker']['sell']
        
        return [priceBid,priceAsk]
    
    def getPriceHuobi(self):
        # http://api.huobi.com/staticmarket/ticker_btc_json.js 
        connection = httplib.HTTPSConnection("api.huobi.com")
        connection.request("GET","/staticmarket/ticker_btc_json.js")
        response = connection.getresponse()
        jsonResponse = response.read()
        infoPrices = json.loads(jsonResponse)
        
        priceBid = infoPrices['ticker']['buy']
        priceAsk = infoPrices['ticker']['sell']
        
        return [priceBid,priceAsk]
    
    def getPriceBitfinex(self):
        # https://api.bitfinex.com/v1/pubticker/:symbol
        connection = httplib.HTTPSConnection("api.bitfinex.com")
        connection.request("GET","/v1/pubticker/btcusd")
        response = connection.getresponse()
        jsonResponse = response.read()
        infoPrices = json.loads(jsonResponse)
        
        priceBid = infoPrices['bid']
        priceAsk = infoPrices['ask']
        
        return [priceBid,priceAsk]

        print dataPrice[4]['USD']['bid']
        print dataPrice[4]['USD']['ask']
    
    def getPriceLakeBTC(self):
        # https://www.LakeBTC.com/api_v1/ticker
        connection = httplib.HTTPSConnection("www.LakeBTC.com")
        connection.request("GET","/api_v1/ticker")
        response = connection.getresponse()
        jsonResponse = response.read()
        infoPrices = json.loads(jsonResponse)
    
        priceBid = infoPrices['USD']['bid']
        priceAsk = infoPrices['USD']['ask']
        
        return [priceBid,priceAsk]


traker = TrakerBitcoinBollinger()
traker.initTraker()
traker.activateTraker(0)


def isExistTwitterConfigFile():
    import os
    return os.path.isfile("./TwitterAPI.dat")
    
def testTweepy():
    import tweepy
    auth = tweepy.OAuthHandler("","")
    auth.set_access_token("", "")
    
    api = tweepy.API(auth)
    
    api.send_direct_message(user = "lesenic", text = "TEST")



# testGetPrice()
# testTweepy()
# testEmail()
    