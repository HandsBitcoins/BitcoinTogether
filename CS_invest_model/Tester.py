import DummyAPI
import ClosimStatistician
import ClosimInnerTrader
import ClosimOuterTrader

import time
import cProfile

def test():
    fp = open("inter.csv",'w')
    fp.close()
    listTime = []
    dumAPI = DummyAPI.DummyAPI()
    cloStat = ClosimStatistician.ClosimStatistician(dumAPI)
    cloin = ClosimInnerTrader.ClosimInnerTrader(dumAPI)
    clOut = ClosimOuterTrader.ClosimOuterTrader(dumAPI)
    
    initBal = int(cloin.getSumOfTotalCoins()*dumAPI.nowPriceBid)+dumAPI.getCashBalance()    
    streamLength = dumAPI.getStreamLength()
    
    for i in range(streamLength):
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
        sumAmount = dumAPI.bitBalance
        totalCash = int(sumAmount*infos[1].price) + dumAPI.cashBalance
        timeEnd = time.time()
        percent = float(totalCash-initBal)/float(initBal)*100.0
        print i, dumAPI.nowPriceAsk, dumAPI.nowPriceBid, timeEnd-timeStart, totalCash, cloin.getSumOfTotalCoins(), sumAmount, dumAPI.getCashBalance(), percent 
        listTime.append(timeEnd-timeStart)
        newCompound = [str(i), str(dumAPI.nowPriceBid), str(totalCash), str(sumAmount), str(percent)]
        fp = open("inter.csv",'a')
        fp.write(','.join(newCompound)+'\n')
        fp.close()
        
        if abs(cloin.getSumOfTotalCoins()-sumAmount) > 0.000000001 or dumAPI.cashBalance < 0:            
            break

    cntOverTime = 0
    fp = open("time.csv",'w')
    for eachT in listTime:
        fp.write(str(eachT)+"\n")
        if eachT > 1.0:
            cntOverTime += 1
    fp.close()
    import numpy    
    print streamLength, sum(listTime), numpy.mean(listTime), numpy.std(listTime), cntOverTime
    #     if infos[0].isBuy:
    #         print ""
    
    
test()
