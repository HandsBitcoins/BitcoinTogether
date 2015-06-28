import math
import random

import ClosimCommonMessageObjects
import ClosimBalanceManager

class ClosimInnerTrader(ClosimBalanceManager.ClosimBalanceManager):
    def __init__(self,API):
        self.isPrevBuy = True
        self.prevPriceCrest = 0.0
        self.prevPriceTrough = 0.0
        self.countFuse = 1.0
                                   
        self.dictMenu = {"buy": 0, 
                         "sell": 1}
        
        ClosimBalanceManager.ClosimBalanceManager.__init__(self,API)

    def actInnerTrader(self,infos):
        listQuery = []

        listQuery += self.buy(infos[0])
        listQuery += self.sell(infos[1])
        
        listQuery = self.fuseQuery(listQuery)
        
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
                                
#                 print rateBasic, rateRandom, rateFinal, self.cashBalances, infoBuy.priceNow, self.countFuse
                amtBuy = rateFinal*self.API.getCashBalance()/infoBuy.priceNow/math.floor(self.countFuse/10 + 1.0)                
                amtBuy = min(amtBuy,infoBuy.amountAsk)
                
                infoQuery = self.generateInfoBalanceByVariables(amtBuy,infoBuy.priceNow,priceExpectedRising)                
                self.registerBalanceByInfoBalance(infoQuery)
                infoRegistedBalance = self.getProcessBalanceInfo()                
                
                listBuyQuery.append(infoRegistedBalance[-1])
            
            self.isPrevBuy = priceExpectedProfit < infoBuy.priceNow+feeExpected
                    
        return listBuyQuery
        
    def sell(self,infoSell):
        listSellQuery = []
           
        listInfoBalance = self.searchBalanceToSell(infoSell.price)        
        
        amtTotalSell = 0.0
        
        #sum sell amount until amountNowBid
        for eachInfoBalance in listInfoBalance:            
            eachInfoBalance.price = infoSell.price 
            amtTotalSell += eachInfoBalance.nextSellAmount
            
            if amtTotalSell > infoSell.amount:
                eachInfoBalance.nextSellAmount -= amtTotalSell - infoSell.amount                
                listSellQuery.append(eachInfoBalance)
                break
            else: 
                listSellQuery.append(eachInfoBalance)
                
        return listSellQuery

    def fuseQuery(self,listQuery):
        if len(listQuery) < 2:
            return listQuery

        if listQuery[0].state == 'Process':
            amtBuyTransSell = listQuery[0].nextSellAmount
            isBuyProcessed = False
            
            newListQuery = []
            for eachQuery in listQuery[1:]:
                if amtBuyTransSell > eachQuery.nextSellAmount:
                    amtBuyTransSell -= eachQuery.nextSellAmount
                    eachQuery.nextSellAmount = 0.0
                    self.proceedBalance(eachQuery.balanceID)
                else:
                    eachQuery.nextSellAmount -= amtBuyTransSell                    
                    self.updateBalanceSellAmt(eachQuery.balanceID,amtBuyTransSell)
                    amtBuyTransSell = 0.0
                    isBuyProcessed = True
                    break
            
            listQuery[0].amount -= amtBuyTransSell
            self.registerBalanceByInfoBalance(listQuery[0],isComplete=True)
                        
            listQuery[0].amount = amtBuyTransSell
            listQuery[0].nextSellAmount = amtBuyTransSell
            self.processBuyBalance(listQuery[0].balanceID,amtBuyTransSell)
            
            if not isBuyProcessed:
                newListQuery.append(listQuery[0])
            else:
                for eachQuery in listQuery[1:]:
                    if eachQuery.nextSellAmount != 0.0:                        
                        newListQuery.append(eachQuery)
            
            return newListQuery
        
        return listQuery
    
# import DummyAPI
# duAP = DummyAPI.DummyAPI()
# cloIn = ClosimInnerTrader(duAP)
# # cloIn.createOrderTable()
#     
# iS = ClosimCommonMessageObjects.InfoSell(270000, 1.2) 
# 
# res = cloIn.sell(iS)
# for eares in res:
#     print eares
#     
# iB = cloIn.generateInfoBalanceByVariables(1.5,270100,275000)
# 
# listQ = [iB]
# listQ += res
# 
# res2 = cloIn.fuseQuery(listQ)
# for eares in res2:
#     print eares


    

