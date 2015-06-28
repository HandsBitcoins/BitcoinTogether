import math

class ClosimCalculator(object):
    def __init__(self,API):
        self.API = API
        self.rateFee = API.rateFee
        self.unitCurrency = API.unitCurrency        
                
    def calPriceExpected(self,priceCrest,priceTrough):
        valAmplitude = abs(priceCrest-priceTrough)
        ratioExpected = self.getExpectationRatio(valAmplitude)
        
        priceExpected = priceTrough + valAmplitude*ratioExpected
        
#         print priceCrest, priceTrough, valAmplitude, ratioExpected, priceExpected
        
        return self.calPriceQuantized(priceExpected)
        
    def getExpectationRatio(self,valAmplitude):
        return 103.79133081279231**(-valAmplitude/8559.704161857346)+0.26960604565535746        
        
    def calFeeCost(self,priceExpectedRising,priceNow):
        priceTotal =  self.calPriceExpectedProfit(priceExpectedRising,priceNow)
        priceTotal += priceNow
        
        return priceTotal*self.rateFee
    
    def calPriceExpectedProfit(self,priceExpectedRising,priceNow):
        priceExpectedProfit = 0.0
        for i in range(5):
            priceExpectedProfit += self.calRateSell(i)*self.calPriceSell(priceExpectedRising,priceNow,i)
            
        return priceExpectedProfit
        
    def calRateSell(self,numStep=0):
        return -1.0*((numStep**3.0)-6.0*(numStep**2.0)+5.0*numStep)/60.0+0.1
    
    def calPriceSell(self,priceExpectedRising,priceNow,numStep=0):
        stepPrice = (priceExpectedRising-priceNow)/5.0
        priceSteped = priceNow+stepPrice*(numStep+1)
        
        return self.calPriceQuantized(priceSteped)
    
    def calPriceQuantized(self,priceReal,isCeil=True):
        if isCeil:
            priceSellUnit = math.ceil(priceReal/self.unitCurrency)
        else:
            priceSellUnit = math.floor(priceReal/self.unitCurrency)
            
        priceQuantized = priceSellUnit*self.unitCurrency
    
        return priceQuantized
    
    def getRateToSell(self, numStep):
        #step = 5 => 30%
        #step = 4 => 30%
        #step = 3 => 20%
        #step = 2 => 10%
        #step = 1 => 10%
        #-1/6*(x^3-6x^2+5x-6)
        
        return -1.0*((numStep**3.0)-6.0*(numStep**2.0)+5.0*numStep)/60.0+0.1    
    
    
    
        
# for valAmplitude in range(0,10000,100):
#     print valAmplitude, 103.79133081279231**(-valAmplitude/8559.704161857346)