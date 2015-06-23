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
        
        self.dictBuyQuery = {0: "Menu", 
                             1: "Amount",
                             2: "PriceNow",
                             3: "Expected"}
        
        self.dictSellQuery = {0: "Menu", 
                              1: "Amount",
                              2: "Price",
                              3: "ID"}
                
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
            priceExpectedRising = self.calPriceExpected(infoBuy.priceCrest, infoBuy.priceTrough)
            
            #cal expectation profit
            priceExpectedProfit = self.calPriceExpectedProfit(priceExpectedRising,infoBuy.priceNow)
            feeExpected = self.calFeeCost(priceExpectedRising,infoBuy.priceNow)
            
            #if there profit
            if priceExpectedProfit > infoBuy.priceNow+feeExpected:
                #cal buy amount
                rateBasic = self.getExpectationRatio(infoBuy.priceCrest-infoBuy.priceTrough)**3
                rateRandom = random.uniform(0.5, 1.0)                
                rateFinal = rateRandom*rateBasic/10.0
                
                amtBuy = rateFinal*self.cashBalances/infoBuy.priceNow/self.countFuse
                
                #return buy query
                #Sell, amount, price
                query = [self.dictMenu["buy"],amtBuy,infoBuy.priceNow,priceExpectedRising]
                listBuyQuery.append(query)
            
            self.isPrevBuy = priceExpectedProfit < infoBuy.priceNow+feeExpected
                    
        return listBuyQuery
        
    def sell(self,infoSell):
        listSellQuery = []
           
        listFetchQuery = self.balanceManager.searchBalanceToSell(infoSell.priceBid)
        
        #sum sell amount until amountNowBid
        for eachFetchQuery in listFetchQuery:            
            processQuery = [self.dictMenu["sell"]]
            processQuery.append(eachFetchQuery[self.balanceManager.dictBalanceDBIndex["nextSellAmount"]])
            processQuery.append(eachFetchQuery[self.balanceManager.dictBalanceDBIndex["nextSellPrice"]])
            processQuery.append(eachFetchQuery[self.balanceManager.dictBalanceDBIndex["balanceID"]])
            listSellQuery.append(processQuery)
        
        return listSellQuery
        
    def fuseQuery(self,listQuery,infoSell):
        if len(listQuery) < 2:
            return listQuery
            
        if listQuery[0][self.dictQuery["Menu"]] == self.dictMenu["buy"]:
            amtBuyTransSell = listQuery[0][self.dictQuery["Amount"]]
            isBuyProcessed = False
            
            newListQuery = []
            for eachQuery in listQuery[1:]:
                if amtBuyTransSell > eachQuery[self.dictQuery["Amount"]]:
                    amtBuyTransSell -= eachQuery[1]
                    eachQuery[1] = 0.0
                    self.balanceManager.processBalanceNextStep(eachQuery[self.dictQuery["ID"]])
                else:
                    eachQuery[1] -= amtBuyTransSell
                    amtBuyTransSell = 0.0
                    self.balanceManager.updateBalanceSellAmt(eachQuery[self.dictQuery["Amount"]],eachQuery[self.dictQuery["ID"]])
                    isBuyProcessed = True
                    break
            
            listQuery[0][self.dictQuery["Amount"]] -= amtBuyTransSell
            infoNewBalance = self.generateInfoBalanceByQuery(listQuery[0])
            self.balanceManager.registerBalanceByInfoBalance(infoNewBalance)
            
            if not isBuyProcessed:
                listQuery[0][self.dictQuery["Amount"]] = amtBuyTransSell
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
    

