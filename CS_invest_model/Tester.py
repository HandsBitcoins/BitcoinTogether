import DummyAPI
import ClosimStatistician
import ClosimInnerTrader
import ClosimOuterTrader
import cProfile

def test():
    dumAPI = DummyAPI.DummyAPI()
    cloStat = ClosimStatistician.ClosimStatistician(dumAPI)
    cloin = ClosimInnerTrader.ClosimInnerTrader(dumAPI)
    clOut = ClosimOuterTrader.ClosimOuterTrader(dumAPI)
    
    initBal = int(cloin.getSumOfTotalCoins()*dumAPI.nowPriceBid)+dumAPI.getCashBalance()
    
    for i in range(50):
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
        print i, totalCash, sumAmount, dumAPI.getCashBalance(), float(totalCash-initBal)/float(initBal)/100.0    
    
    #     if infos[0].isBuy:
    #         print ""
    
cProfile.run(test())