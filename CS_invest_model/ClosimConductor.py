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

import atexit

@atexit.register
def finalizer():
	print "You are now leaving the Python sector."    
#     stats.disconnectDataBase()

testStreamProcessing("./korbitKRW.csv")