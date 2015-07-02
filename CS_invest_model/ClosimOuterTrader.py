
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
        self.clearQuery()            
        
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
            
            #eachOrder.printBalanceInfo()
            #print infoFill
            
            if infoFill.amount == eachOrder.nextSellAmount:
                #print "proceed normally"
                self.proceedBalance(eachOrder.balanceID)            
            else:
                if eachOrder.state == 'Sell':                    
                    self.updateBalanceComplete(eachOrder.balanceID)
                    if infoFill.amount > 0:
                        #print "update next sell amt"
                        self.updateBalanceSellAmt(eachOrder.balanceID, infoFill.amount)                    
                else:
                    if infoFill.amount > 0:
                        #print "less start"                    
                        self.updateBalanceStart(eachOrder, infoFill.amount)                    
                    else:
#                         print "delete"
                        self.destructBalance(eachOrder.balanceID)
        self.clearQuery()
                    
        return False
                    
                    
                
            
            
        
        
        
        
        
        
    
        
        
        
            
        