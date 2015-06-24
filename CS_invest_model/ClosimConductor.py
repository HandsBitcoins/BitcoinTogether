import ClosimStatistician
import os

os.remove("./RAF.db")
stats = ClosimStatistician.ClosimStatistician()
stats.init()

def excuteClosim():
	pass
	
def runStatistician():
	listData = [] #[priceBid,isPeakFall,priceAsk,nowFall,avgFall,stdFall]
	
	return listData	

def getPriceStreamFromCSV(nameFile):
	fileOpened = open(nameFile)
	listRawAll = fileOpened.readlines()
	fileOpened.close()
	
	listPrice = []
	
	for eachLine in listRawAll:
		listLine = eachLine.split(',')
		listPrice.append(float(listLine[1]))
		
	return listPrice
	
def testStreamProcessing(nameFile):
	listStream = getPriceStreamFromCSV(nameFile)

	stats.createPriceTable("testStream")
	for eachData in listStream:
		stats.proceedStep(eachData)
	stats.clearQuery()
	
	stats.selectAllTable()

import atexit

@atexit.register
def finalizer():
	print "You are now leaving the Python sector."    
#     stats.disconnectDataBase()

testStreamProcessing("./korbitKRW.csv")