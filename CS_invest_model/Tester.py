import DummyAPI
import ClosimStatistician
import ClosimBalanceManager
import ClosimInnerTrader

dumAPI = DummyAPI.DummyAPI()
cloStat = ClosimStatistician.ClosimStatistician(dumAPI)
cloBal = ClosimBalanceManager.ClosimBalanceManager(dumAPI)
cloin = ClosimInnerTrader.ClosimInnerTrader(dumAPI,cloBal) 

for _ in range(100):
    infos = cloStat.getInfoForInnerTrader()
        
#     if infos[0].isBuy:
#         print infos[0]
#         print infos[1]
#         print ""
        
    listQuery = cloin.actInnerTrader(infos)
    if len(listQuery)>0:
        print infos[0]
        print listQuery
        print ""
        
#     if infos[0].isBuy:        
#         print ""