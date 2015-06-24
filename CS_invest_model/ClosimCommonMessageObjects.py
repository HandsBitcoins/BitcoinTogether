class InfoBuy(object):
    def __init__(self, isBuy, priceCrest, priceTrough, priceNow, amountAsk):
        self.isBuy = isBuy
        self.priceCrest = priceCrest
        self.priceTrough = priceTrough
        self.priceNow = priceNow
        self.amountAsk = amountAsk
        
    def __str__(self):
        return  "IsBuy: " + str(self.isBuy) + ", PriceCrest: " + str(self.priceCrest) + ", PriceTrough: " + str(self.priceTrough) + ", PriceNow: " + str(self.priceNow) + ", AmountAsk: " + str(self.amountAsk)  

class InfoSell(object):
    def __init__(self, priceBid, amountBid, balanceID=-1):        
        self.priceBid = priceBid
        self.amountBid = amountBid
        self.balanceID = balanceID
        
    def __str__(self):
        return "PriceBid: " + str(self.priceBid) + ", AmountBid: " + str(self.amountBid) + ", BalanceID: " + str(self.balanceID)
        
class InfoMarket(object):
    def __init__(self, priceAsk=0.0, priceBid=0.0, amountAsk=0.0, amountBid=0.0):
        self.priceBid = priceBid
        self.priceAsk = priceAsk
        self.amountBid = amountBid
        self.amountAsk = amountAsk        
  
class InfoBalance(object):
    def __init__(self):
        pass
        
    def __str__(self):
        listStr = []
        listStr.append(str(self.amountBuy))
        listStr.append(str(self.priceBuy))
        listStr.append(str(self.priceExpected))
        listStr.append(str(self.nowSteps))
        listStr.append(str(self.nextSellAmount))
        listStr.append(str(self.nextSellPrice))
        
        return ', '.join(listStr)
    
    def initByPriceAndAmount(self, amountBuy, priceBuy, priceExpected):
        import ClosimCalculator
        self.balanceID = -1
        
        self.amountBuy = amountBuy
        self.priceBuy = priceBuy
        self.priceExpected = priceExpected
        
        self.nowSteps = 0
        
        cloCal = ClosimCalculator.ClosimCalculator()        
        self.nextSellAmount = cloCal.calRateSell(self.nowSteps)*self.amountBuy
        self.nextSellPrice = cloCal.calPriceSell(self.priceExpected, self.priceBuy, self.nowSteps)
    
    def initByData(self, amountBuy, priceBuy, priceExpected, nowSteps, nextSellAmount, nextSellPrice, balanceID=-1):
        #balanceID, amountBuy, priceBuy, priceExpected, nowSteps, nextSellAmount, nextSellPrice        
        self.balanceID = balanceID
        self.amountBuy = amountBuy
        self.priceBuy = priceBuy
        self.priceExpected = priceExpected
        self.nowSteps = nowSteps
        self.nextSellAmount = nextSellAmount
        self.nextSellPrice = nextSellPrice
        
    def initByList(self,listData):
        sizeList = len(listData)
    
        if sizeList == 6:
            self.balanceID = -1
            self.amountBuy = listData[0]
            self.priceBuy = listData[1]
            self.priceExpected = listData[2]
            self.nowSteps = listData[3]
            self.nextSellAmount = listData[4]
            self.nextSellPrice = listData[5]
            return True
            
        elif sizeList == 7:    
            self.balanceID = listData[0]
            self.amountBuy = listData[1]
            self.priceBuy = listData[2]
            self.priceExpected = listData[3]
            self.nowSteps = listData[4]
            self.nextSellAmount = listData[5]
            self.nextSellPrice = listData[6]    
            return True
            
        else:
            return False