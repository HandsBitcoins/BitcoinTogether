import math
import random
import sqlite3

import scipy.stats

import ClosimCommonMessageObjects

class closimInnerTrader(object):
    def __init__(self):
        self.nameDB = "balance.db"
        self.connectDatabase()
    
    def __del__(self):
        self.disconnectDatabase()
    
    def init(self,API):
        self.rateFee = API.rateFee
        self.unitCurreny = API.unitCurreny
        self.cashBalances = 0.0
        
        self.isPrevBuy = True
        self.prevPriceCrest = 0.0
        self.prevPriceTrough = 0.0
        self.countFuse = 1.0

        self.dictBalanceDBIndex = {balanceID:       0,
                                   amountBuy:       1,
                                   priceBuy:        2,
                                   priceExpected:   3,
                                   nowSteps:        4,
                                   nextSellAmount:  5,
                                   nextSellPrice:   6}
                                   
        self.dictMenu = {0: "buy",
                                1: "sell"}
                
    def testBuy(self):
        self.buy(infoBuy)
                
    def actInnerTrader(self,infoSell,infoBuy):
        listQuery = []

        listQuery += self.buy(infoBuy)
        listQuery += self.sell(infoSell)
        
        self.fuseQuery(listQuery,infoSell)
        
        return listQuery
                
#   wave crest and trough
    def buy(self,infoBuy):
        listBuyQuery = []
        if not infoBuy.isBuy:
            return listBuyQuery
        else:
            if self.isPrevBuy:
                if self.prevPriceCrest > infoBuy.priceCrest:
                    infoBuy.priceCrest = self.prevPriceCrest
                    if self.prevPriceTrough < infoBuy.priceTrough:
                        infoBuy.priceTrough = self.prevPriceTrough
                self.countFuse += 1.0
            else:
                self.countFuse = 1.0
            
            #cal expectation rising up price
            valAmplitude = infoBuy.priceCrest - infoBuy.priceTrough
            rateExpected = self.getExpectationRatio(valAmplitude)
            priceExpectedRising = self.calPriceQuantized(infoBuy.priceTrough+rateExpected*valAmplitude)
            
            #cal expectation profit
            priceExpectedProfit = self.calPriceExpectedProfit(priceExpectedRising,infoBuy.priceNow)
            feeExpected = self.calFeeCost(priceExpectedRising,infoBuy.priceNow)
            
            #if there profit
            if priceExpectedProfit > infoBuy.priceNow+feeExpected:
                #cal buy amount
                rateBasic = getExpectationRatio(valAmplitude)**3
                rateRandom = random.uniform(0.5, 1.0)                
                rateFinal = rateRandom*rateBasic/10.0
                
                amtBuy = rateFinal*self.cashBalances/infoBuy.priceNow/self.countFuse
                
                #return buy query
                #Sell, amount, price
                query = [self.dictMenu["buy"],amtBuy,infoBuy.priceNow]
                listBuyQuery.append(query)
            
            self.isPrevBuy = priceExpectedProfit < infoBuy.priceNow+feeExpected
        
        return listBuyQuery
    
    def getExpectationRatio(self,valAmplitude):        
        return 103.79133081279231**(-valAmplitude/8559.704161857346)+0.26960604565535746
    
    def calFeeCost(self,priceExpectedRising,priceNow):
        priceTotal =  self.calPriceExpectedProfit(priceExpectedRising,priceNow)
        priceTotal += priceNow
        
        return priceTotal*self.rateFee
    
    def calPriceExpectedProfit(self,priceExpectedRising,priceNow):
        priceExpectedProfit = 0.0
        for i in range(5):
            priceExpectedProfit += self.calRateSell(i)*self.calPriceSell(priceExpectedRising,priceNow,i)
            
        return priceExpectedProfit
        
    def calRateSell(self,numStep=0):
        return -1.0*((numStep**3.0)-6.0*(numStep**2.0)+5.0*numStep)/60.0+0.1
    
    def calPriceSell(self,priceExpectedRising,priceNow,numStep=0):
        stepPrice = (priceExpected-priceNow)/5.0
        priceSteped = priceNow+stepPrice*(numStep+1)
        
        return self.calPriceQuantized(priceSteped)
    
    def calPriceQuantized(self,priceReal,isCeil=True):        
        if isCeil:
            priceSellUnit = math.ceil(priceReal/unitCurrency)
        else:
            priceSellUnit = math.floor(priceReal/unitCurrency)
            
        priceQuantized = priceSellUnit*self.unitCurrency
    
        return priceQuantized
    
    def getRateToSell(self, numStep):
        #step = 5 => 30%
        #step = 4 => 30%
        #step = 3 => 20%
        #step = 2 => 10%
        #step = 1 => 10%
        #-1/6*(x^3-6x^2+5x-6)
        
        return -1.0*((numStep**3.0)-6.0*(numStep**2.0)+5.0*numStep)/60.0+0.1    
    
    def sell(self,infoSell):
        listSellQuery = []
        
        #balanceID, amountBuy, priceBuy, priceExpected, nowSteps, nextSellAmount, nextSellPrice
        self.cursor.execute("SELECT * FROM " + self.nameTable + " WHERE nextSellPrice < " + str(infoSell.priceBid))
        listFetchQuery = self.cursor.fetchall()
        
        #processing
        #sort by price increase order
        listFetchQuery.sort(key=itemgetter(self.dictBalanceDBIndex[nextSellPrice]))
        
        #sum sell amount until amountNowBid
        for eachFetchQuery in listFetchQuery:
            processQuery = [self.dictMenu["sell"],eachFetchQuery[self.dictBalanceDBIndex[nextSellAmount]],eachFetchQuery[self.dictBalanceDBIndex[nextSellPrice]],eachFetchQuery[self.dictBalanceDBIndex[balanceID]]]
            listSellQuery.append(processQuery)
        
        return listSellQuery
        
    def fuseQuery(self,listQuery,infoSell):
        if len(listQuery) < 2:
            return listQuery
            
        if listQuery[0][0] == self.dictMenu["buy"]:
            amtBuyTransSell = listQuery[0][1]
            
            for eachQuery in listQuery[1:]:                
                if amtBuyTransSell > eachQuery[1]:
                    amtBuyTransSell -= eachQuery[1]
                    eachQuery[1] = 0.0
                else:
                    eachQuery[1] -= amtBuyTransSell
                    break
            
            newListQuery = []
            for eachQuery in listQuery[1:]:
                if eachQuery[1] != 0.0:
                    newListQuery.append(eachQuery)
                else:                    
                    self.processBalanceNextStep(eachQuery[3])
                    
            return newListQuery
        
        return listQuery
        
    def processBalanceNextStep(self,balaceID):
        self.cursor.execute("SELECT * FROM " + self.nameTable + " WHERE balaceID = " + str(balaceID))
        listFetchQuery = self.cursor.fetchall()
        
        if len(listFetchQuery) != 1:
            print "Fail to load balance from ID."
            return False
        
        if listFetchQuery[0][self.dictBalanceDBIndex[nowSteps]] != 4:
            self.proceedBalance(listFetchQuery[0])
        else:
            self.destructBalance(balaceID)
        
    def proceedBalance(self,tupleQueried):
        #balanceID, amountBuy, priceBuy, priceExpected, nowSteps, nextSellAmount, nextSellPrice
        balaceID = tupleQueried[self.dictBalanceDBIndex[balanceID]]
        nowSteps = tupleQueried[self.dictBalanceDBIndex[nowSteps]]
        priceExpected = tupleQueried[self.dictBalanceDBIndex[priceExpected]]
        priceBuy = tupleQueried[self.dictBalanceDBIndex[priceBuy]]
        amtBuy = tupleQueried[self.dictBalanceDBIndex[amountBuy]]
        
        priceNext = priceBuy+(priceExpected-priceBuy)/5.0*(nowSteps+1.0)
        priceNextQuntaized = self.calPriceQuantized(priceNext)
        
        amtNext = amtBuy*self.getRateToSell(numSteps+1)

        self.cursor.execute("UPDATE " + self.nameTable + " SET nowSteps = " + str(nowSteps+1) +
                            ", nextSellAmount = " + str(amtNext) + 
                            ", nextSellPrice = " + str(priceNextQuntaized) +
                            " WHERE balaceID = " + str(balaceID))
        
        self.clearQuery()
    
    def destructBalance(self,balaceID):
        self.cursor.execute("DELETE FROM " + self.nameTable + " WHERE balaceID = " + str(balaceID))
        self.clearQuery()
    
    def createPriceTable(self,nameTable):
        #balanceID, amountBuy, priceBuy, priceExpected, nowSteps, nextSellAmount, nextSellPrice
        self.cursor.execute("CREATE TABLE " + nameTable + "(balanceID INTEGER PRIMARY KEY AUTOINCREMENT, amountBuy float, priceBuy float, priceExpected float, nowSteps int, nextSellAmount float, nextSellPrice float)") 
        self.nameTable = nameTable
    
    def connectDatabase(self):
        self.connDB = sqlite3.connect(self.nameDB)
        self.cursor = self.connDB.cursor()
        
    def disconnectDatabase(self):
        self.connDB.commit()
        self.connDB.close()
        
    def clearQuery(self):
        self.connDB.commit()
        

    
def calInverseDownRateByRatio(ratioDown):
    return (1-ratioDown)/ratioDown

def calDigByPrices(pricePeak,priceBuy):
    return pricePeak-priceBuy

def calDigByRatioAndPeak(ratioDown,pricePeak):
    return (1-ratioDown)*pricePeak
    
def calRatioByFallAndNow(valFall,priceNow):
    return float(priceNow)/(float(priceNow)+float(valFall))

def getExpectationRatio(nowDig):
    #6000/1.1062902622635594*^7*103.79133081279231^(-x/8559.704161857346)
    #0.000542353

    #find constant to make 1 in x is zero
    #valZero = scipy.stats.norm(0,devDigs).pdf(0)
    #3ampExpectation = 1.0 - valZero
    
    #mapping   nowDig:avgDigs = x:Sigma(devDigs)
    #valMappingAvgToSigma = float(devDigs)/float(avgDigs)
    #valMapped = float(valMappingAvgToSigma)*float(nowDig)
    #print valMapped, ampExpectation
    
    return 103.79133081279231**(-nowDig/8559.704161857346)+0.26960604565535746

def calMaxRate(ratioDown,valExpect):
    #in defensive strategy
    #1.0 * 30% = 0.30
    #0.8 * 30% = 0.24
    #0.6 * 20% = 0.12
    #0.4 * 10% = 0.04
    #0.2 * 10% = 0.02
    #sum = 0.72
    
    return 0.72*valExpect*calInverseDownRateByRatio(ratioDown)

def calMinRate(ratioDown,valExpect):
    return 0.02*valExpect*calInverseDownRateByRatio(ratioDown)


    
def checkFeeConditionVal(priceNow,valFall,valFeePercent=0.000):
    ratioDown = calRatioByFallAndNow(valFall,priceNow)
    valExpect = getExpectationRatio(valFall)

    #print calMinRate(ratioDown,valExpect) , valFeePercent*(2+calMaxRate(ratioDown,valExpect))
    return calMinRate(ratioDown,valExpect) > valFeePercent*(2+calMaxRate(ratioDown,valExpect))
    
def checkFeeConditionRatio(ratioDown,valExpect,valFeePercent=0.000):
    return getMinRate(ratioDown,valExpect) > valFeePercent*(2+calMaxRate(ratioDown,valExpect))    

def calBuyAmount(fundRemain,valExpect):
    return fundRemain*(valExpect**2)

def getRateToSell(numStep):
    #step = 5 => 30%
    #step = 4 => 30%
    #step = 3 => 20%
    #step = 2 => 10%
    #step = 1 => 10%
    #-1/6*(x^3-6x^2+5x-6)
    
    return -1.0*((numStep**3.0)-6.0*(numStep**2.0)+5.0*numStep)/60.0+0.1
    
def calSellAmount(amountBitCoin,numStep=0):
    return amountBitCoin*getRateToSell(numStep)

def getAccumRateToSell(numStep):
    accum = getRateToSell(numStep)
    for i in range(numStep):
        accum += getRateToSell(i)
    return accum

def calSellPrice(pricePeak,priceBuy,numStep=0,unitCurrency=100.0):
    priceSellReal = (numStep+1)*0.2*calDigByPrices(pricePeak,priceBuy)+priceBuy
    priceSellUnit = math.ceil(priceSellReal/unitCurrency)
    priceSellQuantized = priceSellUnit*unitCurrency
    
    return priceSellQuantized
    
def calFee(price,valFeePercent=0.000):
    return price*valFeePercent
    
def getRealTotalSell(priceNow,valFall,steps=5):
    totalCost = 0.0
    
    for i in range(steps):
        totalCost += calSellPrice(priceNow+valFall,priceNow,i,500.0)*calSellAmount(1.0,i)
        
    return totalCost
    
def calTotalFee(priceNow,valFall,valFeePercent=0.000,steps=5):  
    totalCost = getRealTotalSell(priceNow,valFall,steps)
        
    return (totalCost+priceNow)*valFeePercent

def getRealTotalProfit(priceNow,valFall,valFeePercent=0.000,steps=5):
    #print getRealTotalSell(priceNow,valFall)
    priceSell = getRealTotalSell(priceNow,valFall,steps+1)

    priceNowAcuum = priceNow*getAccumRateToSell(steps)
    fee = calTotalFee(priceNow,valFall,valFeePercent,steps+1)
#     print priceSell, priceNowAcuum, fee
    
    return priceSell - priceNowAcuum - fee

# for i in range(5):
#     valFeePercent = 0.001
#     printData = [[0 for _ in range(20)]for _ in range(61)]
#     fileOpen = open("asd"+str(i)+".csv",'w')
#     fileOpen.write(','+','.join([str(d) for d in range(500,10500,500)])+'\n')
#     fileOpen.close()
#     
#     for pricePeak in range(250000,280500,500):
#         y = (pricePeak-250000)/500
#         for valFall in range(500,10500,500):
#             x = (valFall-500)/500
#             priceNow = pricePeak-valFall
#             ratioDown = calRatioByFallAndNow(valFall,priceNow)
#             valExpect = getExpectationRatio(valFall)
#             printData[y][x] = getRealTotalProfit(priceNow,valFall,valFeePercent,i)
#     
#     fileOpen = open("asd"+str(i)+".csv",'a')
#     for pricePeak in range(250000,280500,500):
#         fileOpen.write(str(pricePeak)+','+','.join([str(h) for h in printData[(pricePeak-250000)/500]])+'\n')    
#     fileOpen.close()


