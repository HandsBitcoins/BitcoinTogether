import DummyAPI
import ClosimStatistician
import ClosimInnerTrader

dumAPI = DummyAPI.DummyAPI()
cloStat = ClosimStatistician.ClosimStatistician(dumAPI)
cloin = ClosimInnerTrader.ClosimInnerTrader(dumAPI)

for _ in range(100):
    infos = cloStat.getInfoForInnerTrader()
        
#     if infos[0].isBuy:
#         print infos[0]
#         print infos[1]
#         print ""
        
    listQuery = cloin.actInnerTrader(infos)
    if len(listQuery)>0:
        print infos[0]
        for eachQ in listQuery:            
            print eachQ
        print ""
        
#     if infos[0].isBuy:        
#         print ""