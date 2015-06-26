class InfoMarketWave(object):
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
        self.price = priceBid
        self.amount = amountBid
        self.balanceID = balanceID        
        self.menu = False
        
    def __str__(self):
        return "PriceBid: " + str(self.price) + ", AmountBid: " + str(self.amount) + ", BalanceID: " + str(self.balanceID)

class InfoBuy(object):
    def __init__(self, priceBuy, priceExpected, amountBuy):
        self.price = priceBuy
        self.priceExpected = priceExpected
        self.amount = amountBuy
        self.menu = True
        
    def __str__(self):
        return  "PriceBuy: " + str(self.price) + ", PriceExpected: " + str(self.priceExpected) + ", AmountAsk: " + str(self.amount)  
        
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
        listStr.append(str(self.amount))
        listStr.append(str(self.price))
        listStr.append(str(self.priceExpected))
        listStr.append(str(self.nowSteps))
        listStr.append(str(self.nextSellAmount))
        listStr.append(str(self.nextSellPrice))
        
        return ', '.join(listStr)
    
    def initByPriceAndAmount(self, amountBuy, priceBuy, priceExpected):
        import ClosimCalculator
        self.balanceID = -1
        
        self.amount = amountBuy
        self.price = priceBuy
        self.priceExpected = priceExpected
        
        self.nowSteps = 0
        
        cloCal = ClosimCalculator.ClosimCalculator()        
        self.nextSellAmount = cloCal.calRateSell(self.nowSteps)*self.amount
        self.nextSellPrice = cloCal.calPriceSell(self.priceExpected, self.price, self.nowSteps)
    
    def initByData(self, amountBuy, priceBuy, priceExpected, nowSteps, nextSellAmount, nextSellPrice, balanceID=-1):
        #balanceID, amount, price, priceExpected, nowSteps, nextSellAmount, nextSellPrice        
        self.balanceID = balanceID
        self.amount = amountBuy
        self.price = priceBuy
        self.priceExpected = priceExpected
        self.nowSteps = nowSteps
        self.nextSellAmount = nextSellAmount
        self.nextSellPrice = nextSellPrice
        
    def initByList(self,listData):
        sizeList = len(listData)
    
        if sizeList == 6:
            self.balanceID = -1
            self.amount = listData[0]
            self.price = listData[1]
            self.priceExpected = listData[2]
            self.nowSteps = listData[3]
            self.nextSellAmount = listData[4]
            self.nextSellPrice = listData[5]
            return True
            
        elif sizeList == 7:    
            self.balanceID = listData[0]
            self.amount = listData[1]
            self.price = listData[2]
            self.priceExpected = listData[3]
            self.nowSteps = listData[4]
            self.nextSellAmount = listData[5]
            self.nextSellPrice = listData[6]    
            return True
            
        else:
            return False