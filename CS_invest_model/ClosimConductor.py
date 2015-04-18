import ClosimStatistician

stats = ClosimStatistician.closimStatistician()

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
	
	open("./graph2015.csv",'w').close()
	
	listStream = getPriceStreamFromCSV(nameFile)
	for eachData in listStream:
		self.proceedStep(eachData)