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
		
		self.connectDataBase()
                
	def connectDataBase(self):
		self.connDB = sqlite3.connect("RAF.db")
		self.cursor = self.connDB.cursor()
	    
	def proceedStep(self,priceAsk):
		self.streamData.append(priceAsk)
	
		if isDesending:
			if self.streamData[-1] > self.streamData[-2] :
				self.isBuy = True
				self.nowDown = self.streamData[0] - self.streamData[-2]
	        
	def getStdDown(self):
	    pass
	
	
	
	def getAvgDown(self):
	    pass
	   
<<<<<<< HEAD
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
		
		from scipy.stats.stats import pearsonr 
		
		rise = []
		fall = []
		
		listStream = self.getPriceStreamFromCSV(nameFile)
		for eachData in listStream:
			dataPrice = self.proceedStep(eachData)
			fall.append(dataPrice[0])
			rise.append(dataPrice[1])
		
		print pearsonr(fall, rise)
		
test = closimStatistician()
test.init()
test.testStreamProcessing("./korbitKRW2015.csv")

		
		
		
		
		
		
		
		
		
=======
>>>>>>> parent of dbc16d4... 처리 시작.
