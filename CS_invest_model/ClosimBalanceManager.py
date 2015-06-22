import ClosimCalculator

class ClosimBalanceManager(ClosimCalculator.closimCalculator):
    def __init__(self):
        self.nameDB = "balance.db"
        self.connectDatabase()
        
        self.dictBalanceDBIndex = {balanceID:       0,
                           amountBuy:       1,
                           priceBuy:        2,
                           priceExpected:   3,
                           nowSteps:        4,
                           nextSellAmount:  5,
                           nextSellPrice:   6}

    def __del__(self):
        self.clearQuery()
        self.disconnectDatabase()
        
    def connectDatabase(self):
        self.connDB = sqlite3.connect(self.nameDB)
        self.cursor = self.connDB.cursor()
        
    def disconnectDatabase(self):
        self.connDB.commit()
        self.connDB.close()
        
    def clearQuery(self):
        self.connDB.commit()
        
    def createPriceTable(self,nameTable):
        #balanceID, amountBuy, priceBuy, priceExpected, nowSteps, nextSellAmount, nextSellPrice
        self.cursor.execute("CREATE TABLE " + nameTable + "(balanceID INTEGER PRIMARY KEY AUTOINCREMENT, amountBuy float, priceBuy float, priceExpected float, nowSteps int, nextSellAmount float, nextSellPrice float)") 
        self.nameTable = nameTable
        
    def searchBalanceToSell(self,priceToSell):
        #balanceID, amountBuy, priceBuy, priceExpected, nowSteps, nextSellAmount, nextSellPrice
        self.cursor.execute("SELECT * FROM " + self.nameTable + " WHERE nextSellPrice < " + str(priceToSell))
        listFetchQuery = self.cursor.fetchall()
        
        #processing
        #sort by price increase order
        listFetchQuery.sort(key=itemgetter(self.dictBalanceDBIndex[nextSellPrice]))
        
        return listFetchQuery
        
    def registerBalance(self,infoBalanceBuy):
        #INSERT INTO TABLE_NAME (column1, column2, column3,...columnN) VALUES (value1, value2, value3,...valueN);
        self.cursor.execute("INSERT INTO " + self.nameTable + "(amountBuy, priceBuy, priceExpected, nowSteps, nextSellAmount, nextSellPrice) VALUES ("  + str(infoBalanceBuy) + ")") 

    def getBalanceInfoByID(self,balanceID):
        self.cursor.execute("SELECT * FROM " + self.nameTable + " WHERE balaceID = " + str(balaceID))
        listFetchQuery = self.cursor.fetchall()
        
        if len(listFetchQuery) != 1:
            print "Fail to load balance from ID."
            return False        
        
    def updateBalanceSellAmt(self,balaceId,amtNext):
        self.cursor.execute("UPDATE " + self.nameTable + "SET nextSellAmount=" + amtNext + " WHERE balaceID = " + str(balaceID))
        

    def processBalanceNextStep(self,balanceID):
        self.getBalanceInfoByID(balanceID)
        
        if listFetchQuery[0][self.dictBalanceDBIndex[nowSteps]] != 4:
            self.proceedBalance(listFetchQuery[0])
        else:
            self.destructBalance(balanceID)
            
    def destructBalance(self,balaceID):
        self.cursor.execute("DELETE FROM " + self.nameTable + " WHERE balaceID = " + str(balaceID))
        self.clearQuery()
        
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