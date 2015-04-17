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
		#self.connectDataBase()
	        
	def connectDataBase(self):
		self.connDB = sqlite3.connect(self.nameDB)
		self.cursor = self.connDB.cursor()
	
	def proceedStep(self,priceAsk):
		self.streamData.append(priceAsk)
	
		nowUp = 0.0
		
		if len(self.streamData) < 2:
			return [0.0, 0.0]
	
		if self.isDesending:
			if self.streamData[-1] > self.streamData[-2]:
				self.isBuy = True
				self.isDesending = False
				self.nowDown = self.streamData[0] - self.streamData[-2]
# 				print "DESEN", self.streamData
				self.streamData = self.streamData[-2:]
				
		else:			
			if self.streamData[-1] < self.streamData[-2]:
				self.isDesending = True				
				nowUp = self.streamData[-2] - self.streamData[0]
# 				print "ASEN ", self.streamData
				self.streamData = self.streamData[-2:]

		dataSet = [self.nowDown, nowUp]
		#self.insertRiseFall(dataSet)

		return dataSet
				
	def insertRiseFall(self,dataSet):
		self.connectDataBase()
			    
	def getStdDown(self):
		pass
	
	def getAvgDown(self):
		pass
	   
	def getPriceStreamFromCSV(self,nameFile):
		fileOpened = open(nameFile)
		listRawAll = fileOpened.readlines()
		fileOpened.close()
		
		listPrice = []
		
		for eachLine in listRawAll:
			listLine = eachLine.split(',')
			listPrice.append(float(listLine[1]))
			
		return listPrice
		
	def testStreamProcessing(self,nameFile):
		
		open("./graph2015.csv",'w').close()
		
		listStream = self.getPriceStreamFromCSV(nameFile)
		for eachData in listStream:
			self.proceedStep(eachData)
		
test = closimStatistician()
test.init()


		
		
		
		
		
		
		
		
		