import math
import random
import sqlite3

import scipy.stats

import ClosimCalculator
import ClosimCommonMessageObjects

class ClosimInnerTrader(ClosimCalculator.ClosimCalculator):
    def __init__(self,API,balanceManager):
        self.isPrevBuy = True
        self.prevPriceCrest = 0.0
        self.prevPriceTrough = 0.0
        self.countFuse = 1.0
                                   
        self.dictMenu = {0: "buy",
                         1: "sell"}
        
        ClosimCalculator.ClosimCalculator.__init__(self,API)
        self.balanceManager = balanceManager
                                    
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
        
    def sell(self,infoSell):
        listSellQuery = []
           
        listFetchQuery = self.manager.searchBalanceToSell(infoSell.priceBid)
        
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
            isBuyProcessed = False
            
            newListQuery = []
            for eachQuery in listQuery[1:]:                
                if amtBuyTransSell > eachQuery[1]:
                    amtBuyTransSell -= eachQuery[1]
                    eachQuery[1] = 0.0
                    self.manager.processBalanceNextStep(eachQuery[3])
                else:
                    eachQuery[1] -= amtBuyTransSell
                    self.manager.updateBalanceSellAmt()
                    isBuyProcessed = True
                    break
            
            if not isBuyProcessed:
                newListQuery.append(listQuery[0])
            
            for eachQuery in listQuery[1:]:
                if eachQuery[1] != 0.0:
                    newListQuery.append(eachQuery)
            
            return newListQuery
        
        return listQuery


    
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
    
# def checkFeeConditionRatio(ratioDown,valExpect,valFeePercent=0.000):
#     return getMinRate(ratioDown,valExpect) > valFeePercent*(2+calMaxRate(ratioDown,valExpect))

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


