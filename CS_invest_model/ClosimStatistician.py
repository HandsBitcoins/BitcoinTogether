import sqlite3

import ClosimCommonMessageObjects

class ClosimStatistician(object):
    def __init__(self, API):
        self.nameDB = "RAF.db"
        self.connectDatabase()
        
        self.isBuy = False
        self.nowDown = 0.0
        self.avgDown = 0.0
        self.stdDown = 0.0

        self.isDesending = False
        self.streamData = []
        self.nowDown = 0.0
        self.nowUp = 0.0
        
        self.priceCrest = 0.0
        self.priceTrough = 0.0
        self.priceNow = 0.0
        
        self.nameTable = ""
        
        self.API = API
    
    def __del__(self):
        self.disconnectDatabase()
                        
    def connectDatabase(self):
        self.connDB = sqlite3.connect(self.nameDB)
        self.cursor = self.connDB.cursor()
        
    def disconnectDatabase(self):
        self.clearQuery()
        self.connDB.close()
    
    def createPriceTable(self,nameTable):        
        self.cursor.execute("CREATE TABLE " + nameTable + "(priceFall float, priceRise float)") 
        self.nameTable = nameTable
        
    def insertRiseFall(self,dataSet):
        self.cursor.execute("INSERT INTO " + self.nameTable + " VALUES(" + str(dataSet[0]) +", "+ str(dataSet[1]) +")") 
        
    def clearQuery(self):
        self.connDB.commit()
        
    def getInfoForInnerTrader(self):
        infoMarket = self.getMarketInfo()
        
        infoBuy = self.proceedStep(infoMarket.priceAsk,infoMarket.amountAsk)
        infoSell = self.getInfoSell(infoMarket)
        
        return infoBuy, infoSell
        
    def getMarketInfo(self):        
        infoMarket = self.API.getMarketInfo()
        return infoMarket
                    
    def proceedStep(self,priceAsk,amtAsk):
        self.isBuy = False
        self.streamData.append(priceAsk)
    
        nowUp = 0.0
        dataSet = [0.0, 0.0]
        
        if len(self.streamData) < 2:
            return self.getInfoBuy(amtAsk)
    
        if self.isDesending:
            if self.streamData[-1] > self.streamData[-2]:
                self.isBuy = True
                self.isDesending = False
                self.priceCrest = self.streamData[0]
                self.priceTrough = self.streamData[-2]
                self.priceNow = self.streamData[-1]
                self.nowDown = self.streamData[0] - self.streamData[-2]
#               print "DESEN", self.streamData
                self.streamData = self.streamData[-2:]
        else:           
            if self.streamData[-1] < self.streamData[-2]:
                self.isDesending = True
                
                nowUp = self.streamData[-2] - self.streamData[0]
#               print "ASEN ", self.streamData
                self.streamData = self.streamData[-2:]
                dataSet = [self.nowDown, nowUp]
#                 self.insertRiseFall(dataSet)
        
        return self.getInfoBuy(amtAsk)
                
    def selectAllTable(self):
        self.cursor.execute("SELECT * FROM " + self.nameTable)
        dataAll = self.cursor.fetchall()
        
        for eachData in dataAll:
            print eachData[0], eachData[1]
            
    def getInfoBuy(self,amtAsk):
        infoBuy = ClosimCommonMessageObjects.InfoMarketWave(self.isBuy, self.priceCrest, self.priceTrough, self.priceNow, amtAsk)        
        return infoBuy
               
    def getInfoSell(self,infoMarket):
        infoSell = ClosimCommonMessageObjects.InfoSell(infoMarket.priceBid,infoMarket.amountBid)        
        return infoSell
               
    def getStdDown(self):
        pass
    
    def getAvgDown(self):
        pass
       


        
        

        
        
        
        
        
        