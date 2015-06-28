
import ClosimBalanceManager

class ClosimOuterTrader(ClosimBalanceManager.ClosimBalanceManager):
    def __init__(self,API):        
        ClosimBalanceManager.ClosimBalanceManager.__init__(self,API)
        
    def actOuter(self,listOrder):        
        existOrder = len(listOrder) > 0 
        if existOrder:
            self.processOrderQuery(listOrder)        
        
        self.updateBalanceDB(existOrder)
        
        return False        
        
    def processOrderQuery(self,listOrder):        
        self.cancelOrder()
        for eachOrder in listOrder:
            
            infoOrder = self.API.registerOrder(eachOrder)
            if infoOrder.success:
                self.updateStateOrdered(infoOrder,eachOrder.balanceID)            
        
    def cancelOrder(self):
        listNotComplete = self.getNotComletedOrders()
        self.API.cancelAllOrder(listNotComplete)
        
        return False
        
    def updateBalanceDB(self,isCanceled):
        listNotComplete = self.getNotComletedOrders()
#         
#         for each in listNotComplete:
#             print "asd"
#             each.printBalanceInfo()
        
        for eachOrder in listNotComplete:
            infoFill = self.API.getFillOrder(eachOrder.orderID)
            if infoFill.amount == eachOrder.nextSellAmount:                
                self.proceedBalance(eachOrder.balanceID)            
            elif isCanceled:
                if eachOrder.state == 'Sell':
                    self.updateBalanceComplete(eachOrder.balanceID)
                    if infoFill.amount > 0:
                        self.updateBalanceSellAmt(eachOrder.balanceID, infoFill.amount)                    
                else:
                    if infoFill.amount > 0:                    
                        self.updateBalanceStart(eachOrder, infoFill.amount)                    
                    else:
                        self.destructBalance(eachOrder.balanceID)
                    
        return False
                    
                    
                
            
            
        
        
        
        
        
        
    
        
        
        
            
        