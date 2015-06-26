
import ClosimBalanceManager

class ClosimOuterTrader(ClosimBalanceManager.ClosimBalanceManager):
    def __init__(self,API):
        self.API = API        
        self.orders = []
    
        self.API.cancelAllOrder()
        
        ClosimBalanceManager.ClosimBalanceManager.__init__(self,API)
        
    def processOrderQuery(self,listOrder):
        pass
        
    def clearInternalOrder(self):
        infoNowOrder = self.API.getOrderInfo()
        
        if len(self.orders) != len(infoNowOrder):
            pass
        
    def updateBalanceDB(self):
        self.API.getFillOrder()
        
        
        
        
        
        
    
        
        
        
            
        