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
	   
