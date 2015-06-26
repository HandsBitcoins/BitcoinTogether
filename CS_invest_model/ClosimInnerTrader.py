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
        
        self.fuseQuery(listQuery)        
        #listQuery = self.getInfoObjects(listQuery)
        
        return listQuery

    def getInfoObjects(self,listQuery):
        listInfoObjects = []
        
        for eachQuery in listQuery:
            if eachQuery[0] == 0:
                #(self, priceBuy, priceExpected, amountBuy):
                buyInfoObject = ClosimCommonMessageObjects.InfoBuy(eachQuery[self.dictBuyQuery["PriceNow"]],eachQuery[self.dictBuyQuery["Expected"]],eachQuery[self.dictBuyQuery["Amount"]])
                listInfoObjects.append(buyInfoObject)
                                
            else:
                #(self, price, amount, balanceID=-1):
                sellInfoObject = ClosimCommonMessageObjects.InfoSell(eachQuery[self.dictSellQuery["Price"]],eachQuery[self.dictSellQuery["Amount"]],eachQuery[self.dictSellQuery["ID"]])
                listInfoObjects.append(sellInfoObject)
                
        return listInfoObjects

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
#                 class InfoBuy(object):
#                     def __init__(self, priceBuy, priceExpected, amountBuy):
                query = ClosimCommonMessageObjects.InfoBuy(infoBuy.priceNow,priceExpectedRising,amtBuy)
                listBuyQuery.append(query)
            
            self.isPrevBuy = priceExpectedProfit < infoBuy.priceNow+feeExpected
                    
        return listBuyQuery
        
    def sell(self,infoSell):
        listSellQuery = []
           
        listFetchQuery = self.searchBalanceToSell(infoSell.price)
        listFetchQuery.sort(key=lambda listFetchQuery: listFetchQuery[self.dictBalanceDBIndex["nextSellPrice"]])
        
        amtTotalSell = 0.0
        
        #sum sell amount until amountNowBid
        for eachFetchQuery in listFetchQuery:
            eachInfoSell = self.convertFetchQueryToInfoSell(eachFetchQuery)            
            amtTotalSell += eachInfoSell.amount
            
            if amtTotalSell > infoSell.amount:
                eachInfoSell.amount -= amtTotalSell - infoSell.amount
                listSellQuery.append(eachInfoSell)                
                break            
            else: 
                listSellQuery.append(eachInfoSell)
                
        return listSellQuery
    
    def convertFetchQueryToInfoSell(self,fetchQuery):
#         class InfoSell(object):
#             def __init__(self, price, amount, balanceID=-1):
        return ClosimCommonMessageObjects.InfoSell(fetchQuery[self.dictBalanceDBIndex["nextSellPrice"]],fetchQuery[self.dictBalanceDBIndex["nextSellAmount"]],fetchQuery[self.dictBalanceDBIndex["balanceID"]])
        
    def fuseQuery(self,listQuery):
        if len(listQuery) < 2:
            return listQuery
                        
        if listQuery[0].menu:                        
            amtBuyTransSell = listQuery[0].amount
            isBuyProcessed = False
            
            newListQuery = []
            for eachQuery in listQuery[1:]:
                if amtBuyTransSell > eachQuery.amount:
                    amtBuyTransSell -= eachQuery.amount
                    eachQuery.amount = 0.0
                    self.proceedBalance(eachQuery.balanceID)
                else:
                    eachQuery.amount -= amtBuyTransSell
                    amtBuyTransSell = 0.0
                    self.updateBalanceSellAmt(eachQuery.amount,eachQuery.balanceID)
                    isBuyProcessed = True
                    break
            
            listQuery[0].amount -= amtBuyTransSell
            infoNewBalance = self.generateInfoBalanceByQuery(listQuery[0])
            self.registerBalanceByInfoBalance(infoNewBalance)
            
            if not isBuyProcessed:
                listQuery[0].amount = amtBuyTransSell
                newListQuery.append(listQuery[0])
            else:
                for eachQuery in listQuery[1:]:
                    if eachQuery.amount != 0.0:
                        newListQuery.append(eachQuery)

            return newListQuery
        
        return listQuery
    
# import DummyAPI
# duAP = DummyAPI.DummyAPI()
# cloIn = ClosimInnerTrader(duAP)
## cloIn.createOrderTable()
#     
# iS = ClosimCommonMessageObjects.InfoSell(270000, 1.2)

# 
# res = cloIn.sell(iS)
# for eares in res:
#     print eares
#     
# iB = ClosimCommonMessageObjects.InfoBuy(270100,275000,1.5)
# 
# listQ = [iB]
# listQ += res
# 
# res2 = cloIn.fuseQuery(listQ)
# for eares in res2:
#     print eares


    

