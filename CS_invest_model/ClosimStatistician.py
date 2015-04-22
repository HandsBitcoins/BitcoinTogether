import sqlite3

class InfoBuy(object):
    def __init__(self,isBuy, priceCrest, priceTrough, priceNow):
        self.isBuy = isBuy
        self.priceCrest = priceCrest
        self.priceTrough = priceTrough
        self.priceNow = priceNow
    
class ClosimStatistician(object):
    def __init__(self):
        self.nameDB = "RAF.db"
        self.connectDataBase()
    
    def __del__(self):
        self.disconnectDataBase()    
    
    def init(self):
        self.isBuy = False
        self.nowDown = 0.0
        self.avgDown = 0.0
        self.stdDown = 0.0

        self.isDesending = False
        self.streamData = []
        self.nowDown = 0.0
        self.nowUp = 0.0
        
        self.nameTable = ""
                        
    def connectDataBase(self):
        self.connDB = sqlite3.connect(self.nameDB)
        self.cursor = self.connDB.cursor()
        
    def disconnectDataBase(self):
        self.connDB.commit()
        self.connDB.close()
    
    def createPriceTable(self,nameTable):        
        self.cursor.execute("CREATE TABLE " + nameTable + "(priceFall float, priceRise float)") 
        self.nameTable = nameTable
        
    def insertRiseFall(self,dataSet):
        self.cursor.execute("INSERT INTO " + self.nameTable + " VALUES(" + str(dataSet[0]) +", "+ str(dataSet[1]) +")") 
        
    def clearQuery(self):
        self.connDB.commit()
        
    def proceedStep(self,priceAsk):
        self.streamData.append(priceAsk)
    
        nowUp = 0.0
        dataSet = [0.0, 0.0]
        
        if len(self.streamData) < 2:
            return dataSet
    
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
                self.insertRiseFall(dataSet)

        return dataSet
                
    def selectAllTable(self):
        self.cursor.execute("SELECT * FROM " + self.nameTable)        
        dataAll = self.cursor.fetchall()
        
        for eachData in dataAll:
            print eachData[0], eachData[1]
            
    def getInfoBuy(self):
        infoBuy = InfoBuy(self.isBuy, self.priceCrest, self.priceTrough, self.priceNow)        
        return infoBuy
           
    def getStdDown(self):
        pass
    
    def getAvgDown(self):
        pass
       

        


        
        
        
        
        
        
        
        
        