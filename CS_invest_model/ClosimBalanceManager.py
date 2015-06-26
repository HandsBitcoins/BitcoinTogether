import sqlite3
import operator

import ClosimCalculator
import ClosimCommonMessageObjects

class ClosimBalanceManager(ClosimCalculator.ClosimCalculator):
    def __init__(self,API):
        self.nameDB = "balance.db"
        self.connectDatabase()
        
        self.dictBalanceDBIndex = {"balanceID":       0,
                                   "amountBuy":       1,
                                   "priceBuy":        2,
                                   "priceExpected":   3,
                                   "nowSteps":        4,
                                   "nextSellAmount":  5,
                                   "nextSellPrice":   6}
        
        ClosimCalculator.ClosimCalculator.__init__(self,API)

    def __del__(self):
        self.clearQuery()
        self.disconnectDatabase()
        
    def connectDatabase(self):
        import os
        existDB = os.path.isfile(self.nameDB)
        
        self.connDB = sqlite3.connect(self.nameDB)
        self.cursor = self.connDB.cursor()
        
        self.namePriceTable = "BITCOIN_BALANCE"
        self.nameOrderTable = "ORDER_LIST"
        
        if not existDB:
            self.createPriceTable(self.namePriceTable)
            self.createOrderTable(self.nameOrderTable)
        
    def disconnectDatabase(self):
        self.connDB.commit()
        self.connDB.close()
        
    def clearQuery(self):
        self.connDB.commit()
        
    def createPriceTable(self,nameTable="BITCOIN_BALANCE"):
        #balanceID, amountBuy, priceBuy, priceExpected, nowSteps, nextSellAmount, nextSellPrice
        self.cursor.execute("CREATE TABLE " + nameTable + "(balanceID INTEGER PRIMARY KEY AUTOINCREMENT, amountBuy float, priceBuy float, priceExpected float, nowSteps int, nextSellAmount float, nextSellPrice float)")        
        self.clearQuery()
        
    def createOrderTable(self,nameTable="ORDER_LIST"):
        self.cursor.execute("CREATE TABLE " + nameTable + "(orderID INTEGER PRIMARY KEY, balanceID INTEGER, amount float, state TEXT)")
        self.clearQuery()

    def registerBalanceByInfoBalance(self,infoBalanceBuy):
        #INSERT INTO TABLE_NAME (column1, column2, column3,...columnN) VALUES (value1, value2, value3,...valueN);        
        self.cursor.execute("INSERT INTO " + self.namePriceTable + "(amountBuy, priceBuy, priceExpected, nowSteps, nextSellAmount, nextSellPrice) VALUES ("  + str(infoBalanceBuy) + ")")
        self.clearQuery() 

    def searchBalanceToSell(self,priceToSell):        
        #balanceID, amountBuy, priceBuy, priceExpected, nowSteps, nextSellAmount, nextSellPrice
        self.cursor.execute("SELECT * FROM " + self.namePriceTable + " WHERE nextSellPrice < " + str(priceToSell))
        listFetchQuery = self.cursor.fetchall()
        
        #processing
        #sort by price increase order
        listFetchQuery.sort(key=operator.itemgetter(self.dictBalanceDBIndex["nextSellPrice"]))
        
        return listFetchQuery        
    
    def getBalanceInfoByID(self,balanceID):       
        self.cursor.execute("SELECT * FROM " + self.namePriceTable + " WHERE balanceID = " + str(balanceID))
        listFetchQuery = self.cursor.fetchall()
        
        if len(listFetchQuery) != 1:
            print "Fail to load balance from ID."
            return False
        
        return listFetchQuery[0]
        
    def proceedBalance(self,balanceID):
        infoQueriedBalance = self.getBalanceInfoByID(balanceID) 
        
        if infoQueriedBalance[self.dictBalanceDBIndex["nowSteps"]] != 4:
            self.processBalanceNextStep(infoQueriedBalance)
        else:
            self.destructBalance(balanceID)
            
    def destructBalance(self,balaceID):
        self.cursor.execute("DELETE FROM " + self.namePriceTable + " WHERE balanceID = " + str(balaceID))
        self.clearQuery()
        
    def processBalanceNextStep(self,tupleQueried):        
        
        #balanceID, amountBuy, priceBuy, priceExpected, nowSteps, nextSellAmount, nextSellPrice
        balanceID = tupleQueried[self.dictBalanceDBIndex["balanceID"]]
        nowSteps = tupleQueried[self.dictBalanceDBIndex["nowSteps"]]
        priceExpected = tupleQueried[self.dictBalanceDBIndex["priceExpected"]]
        priceBuy = tupleQueried[self.dictBalanceDBIndex["priceBuy"]]
        amtBuy = tupleQueried[self.dictBalanceDBIndex["amountBuy"]]
        
#         priceNext = priceBuy+(priceExpected-priceBuy)/5.0*(nowSteps+1.0)
        priceNext = self.calPriceSell(priceExpected, priceBuy, nowSteps+1)
        amtNext = amtBuy*self.getRateToSell(nowSteps+1)

        self.cursor.execute("UPDATE " + self.namePriceTable + " SET nowSteps = " + str(nowSteps+1) +
                            ", nextSellAmount = " + str(amtNext) + 
                            ", nextSellPrice = " + str(priceNext) +
                            " WHERE balanceID = " + str(balanceID))
        
        self.clearQuery()

    def updateBalanceSellAmt(self,balanceID,newAmount):        
        self.cursor.execute("UPDATE " + self.namePriceTable + " SET nextSellAmount = " + str(newAmount) + " WHERE balanceID = " + str(balanceID))
        self.clearQuery()
        
    def generateInfoBalanceByQuery(self,queryOrder):
        #amountBuy, priceBuy, priceExpected, nowSteps, nextSellAmount, nextSellPrice        
        listData = []
        listData.append(queryOrder.amount)          #listData[0]
        listData.append(queryOrder.price)           #listData[1]
        listData.append(queryOrder.priceExpected)   #listData[2]
        listData.append(0)
        listData.append(self.calRateSell(0)*listData[0])
        listData.append(self.calPriceSell(listData[2], listData[1], 0))
        
        infoBalance = ClosimCommonMessageObjects.InfoBalance()
        infoBalance.initByList(listData)
        
        return infoBalance
    
    def getNotComletedOrders(self):
        self.cursor.execute("SELECT * FROM " + self.nameOrderTable + " WHERE state like 'READY'")
        listFetchQuery = self.cursor.fetchall()        
        
        return listFetchQuery
# import DummyAPI
#         
# dumAPI = DummyAPI.DummyAPI()
# clobalman = ClosimBalanceManager(dumAPI)
# 
# listQuery = clobalman.searchBalanceToSell(265000)
# print listQuery
# 
# clobalman.proceedBalance(3)

