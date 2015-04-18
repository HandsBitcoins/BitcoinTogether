import sqlite3

class closimStatistician(object):
    def __init__(self):
        pass
    
    def init(self):
        self.isBuy = False
        self.nowDown = 0.0
        self.avgDown = 0.0
        self.stdDown = 0.0

        self.isDesending = False
        self.streamData = []
        self.nowDown = 0.0
        self.nowUp = 0.0
        
        self.nameDB = "RAF.db"
        self.nameTable = ""
        
        self.connectDataBase()
                
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
           
    def getStdDown(self):
        pass
    
    def getAvgDown(self):
        pass
       

        


        
        
        
        
        
        
        
        
        