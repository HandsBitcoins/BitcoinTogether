import DummyAPI
import ClosimStatistician
import ClosimInnerTrader
import ClosimOuterTrader

import time
import cProfile

def test():
    dumAPI = DummyAPI.DummyAPI()
    cloStat = ClosimStatistician.ClosimStatistician(dumAPI)
    cloin = ClosimInnerTrader.ClosimInnerTrader(dumAPI)
    clOut = ClosimOuterTrader.ClosimOuterTrader(dumAPI)
    
    initBal = int(cloin.getSumOfTotalCoins()*dumAPI.nowPriceBid)+dumAPI.getCashBalance()
    
    for i in range(5000):
        timeStart = time.time()
        infos = cloStat.getInfoForInnerTrader()
            
    #     if infos[0].isBuy:
    #         print infos[0]
    #         print infos[1]
    #         print ""
        
        listQuery = cloin.actInnerTrader(infos)
    #     if len(listQuery)>0:
    #         print "Inner Query"
    #         for eachQ in listQuery:
    #             eachQ.printBalanceInfo()
    #         print ""
            
        clOut.actOuter(listQuery)
        sumAmount = cloin.getSumOfTotalCoins()
        totalCash = int(sumAmount*infos[1].price) + dumAPI.getCashBalance()
        timeEnd = time.time()
        print i, timeEnd-timeStart, totalCash, sumAmount, dumAPI.getCashBalance(), float(totalCash-initBal)/float(initBal)/100.0
            
    
    #     if infos[0].isBuy:
    #         print ""
    
test()
