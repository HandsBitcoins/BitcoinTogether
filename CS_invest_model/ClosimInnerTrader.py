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
                                   
        self.dictMenu = {"buy": 0, 
                         "sell": 1}
        
        self.dictBuyQuery = {"Menu": 0, 
                             "Amount": 1,
                             "PriceNow": 2,
                             "Expected": 3}
        
        self.dictSellQuery = {"Menu": 0, 
                              "Amount": 1,
                              "Price": 2,
                              "ID": 3}
                
        ClosimCalculator.ClosimCalculator.__init__(self,API)
        self.balanceManager = balanceManager

    def actInnerTrader(self,infos):
        listQuery = []

        listQuery += self.buy(infos[0])
        listQuery += self.sell(infos[1])
        
        self.fuseQuery(listQuery)
        
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
            priceExpectedRising = self.calPriceExpected(infoBuy.priceCrest, infoBuy.priceTrough)
            
            #cal expectation profit
            priceExpectedProfit = self.calPriceExpectedProfit(priceExpectedRising,infoBuy.priceNow)
            feeExpected = self.calFeeCost(priceExpectedRising,infoBuy.priceNow)
            
#             print priceExpectedProfit > infoBuy.priceNow+feeExpected, infoBuy.priceCrest, infoBuy.priceTrough, priceExpectedProfit, infoBuy.priceNow, feeExpected, self.countFuse
            
            #if there profit
            if priceExpectedProfit > infoBuy.priceNow+feeExpected:
                #cal buy amount
                rateBasic = self.getExpectationRatio(infoBuy.priceCrest-infoBuy.priceTrough)**4/2.0
                rateRandom = random.uniform(0.5, 1.0)                
                rateFinal = rateRandom*rateBasic
                                
                print rateBasic, rateRandom, rateFinal, self.cashBalances, infoBuy.priceNow, self.countFuse
                amtBuy = rateFinal*self.cashBalances/infoBuy.priceNow/math.floor(self.countFuse/10 + 1.0)
                
                amtBuy = min(amtBuy,infoBuy.amountAsk)
                
                #return buy query
                #Sell, amount, price
                query = [self.dictMenu["buy"],amtBuy,infoBuy.priceNow,priceExpectedRising]
                listBuyQuery.append(query)
            
            self.isPrevBuy = priceExpectedProfit < infoBuy.priceNow+feeExpected
                    
        return listBuyQuery
        
    def sell(self,infoSell):
        listSellQuery = []
           
        listFetchQuery = self.balanceManager.searchBalanceToSell(infoSell.priceBid)
        listFetchQuery.sort(key=lambda listFetchQuery: listFetchQuery[self.balanceManager.dictBalanceDBIndex["nextSellPrice"]])
        
        amtTotalSell = 0.0
        
        #sum sell amount until amountNowBid
        for eachFetchQuery in listFetchQuery:
            processQuery = [self.dictMenu["sell"]]
            processQuery.append(eachFetchQuery[self.balanceManager.dictBalanceDBIndex["nextSellAmount"]])
            processQuery.append(eachFetchQuery[self.balanceManager.dictBalanceDBIndex["nextSellPrice"]])
            processQuery.append(eachFetchQuery[self.balanceManager.dictBalanceDBIndex["balanceID"]])
            
            amtTotalSell += processQuery[self.dictSellQuery["Amount"]]
            
            if amtTotalSell > infoSell.amountBid:
                break
            else: 
                listSellQuery.append(processQuery)
                
        return listSellQuery
        
    def fuseQuery(self,listQuery):
        if len(listQuery) < 2:
            return listQuery
            
        if listQuery[0][self.dictBuyQuery["Menu"]] == self.dictMenu["buy"]:
            
            for eachQ in listQuery:
                print eachQ
            
            amtBuyTransSell = listQuery[0][self.dictBuyQuery["Amount"]]
            isBuyProcessed = False
            
            newListQuery = []
            for eachQuery in listQuery[1:]:
                if amtBuyTransSell > eachQuery[self.dictSellQuery["Amount"]]:
                    amtBuyTransSell -= eachQuery[1]
                    eachQuery[1] = 0.0
                    self.balanceManager.proceedBalance(eachQuery[self.dictSellQuery["ID"]])
                else:
                    eachQuery[1] -= amtBuyTransSell
                    amtBuyTransSell = 0.0
                    self.balanceManager.updateBalanceSellAmt(eachQuery[self.dictSellQuery["Amount"]],eachQuery[self.dictSellQuery["ID"]])
                    isBuyProcessed = True
                    break
            
            listQuery[0][self.dictBuyQuery["Amount"]] -= amtBuyTransSell
            infoNewBalance = self.generateInfoBalanceByQuery(listQuery[0])
            self.balanceManager.registerBalanceByInfoBalance(infoNewBalance)
            
            if not isBuyProcessed:
                listQuery[0][self.dictBuyQuery["Amount"]] = amtBuyTransSell
                newListQuery.append(listQuery[0])
            else:
                for eachQuery in listQuery[1:]:
                    if eachQuery[1] != 0.0:
                        newListQuery.append(eachQuery)

            return newListQuery
        
        return listQuery
    
    def generateInfoBalanceByQuery(self,queryOrder):
        #amountBuy, priceBuy, priceExpected, nowSteps, nextSellAmount, nextSellPrice        
        listData = []
        listData.append(queryOrder[self.dictBuyQuery["Amount"]])        #listData[0]
        listData.append(queryOrder[self.dictBuyQuery["PriceNow"]])      #listData[1]
        listData.append(queryOrder[self.dictBuyQuery["PriceExpected"]]) #listData[2]
        listData.append(0)
        listData.append(self.calRateSell(0)*listData[0])
        listData.append(self.calPriceSell(listData[2], listData[1], 0))
        
        infoBalance = ClosimCommonMessageObjects.InfoBalance()
        infoBalance.initByList(listData)
        
        return infoBalance        
    
    

