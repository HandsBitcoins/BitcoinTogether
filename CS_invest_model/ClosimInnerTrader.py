import math

import scipy.stats

def calInverseDownRateByRatio(ratioDown):
	return (1-ratioDown)/ratioDown

def calDigByPrices(pricePeak,priceBuy):
	return pricePeak-priceBuy

def CalDigByRatioAndPeak(ratioDown,pricePeak):
	return (1-ratioDown)*pricePeak

def getExpectationRatio(nowDig,avgDigs,devDigs):
	#find constant to make 1 in x is zero
	valZero = scipy.stats.norm(0,devDigs).pdf(0)
	ampExpectation = 1.0 - valZero
    
	#mapping   nowDig:avgDigs = x:Sigma(devDigs)
	valMappingAvgToSigma = float(devDigs)/float(avgDigs)
	valMapped = float(valMappingAvgToSigma)*float(nowDig)
	#print valMapped, ampExpectation

	return ampExpectation + scipy.stats.norm(0,devDigs).pdf(valMapped)

def calMaxRate(ratioDown,valExpect):
	#in defensive strategy
	#1.0 * 30% = 0.30
	#0.8 * 30% = 0.24
	#0.6 * 20% = 0.12
	#0.4 * 10% = 0.04
	#0.2 * 10% = 0.02
	#sumattion = 0.72
	
	return 0.72*valExpect*calInverseDownRateByRatio(ratioDown)

def calMinRate(ratioDown,valExpect):
	return 0.02*valExpect*calInverseDownRateByRatio(ratioDown)
   
def checkFeeCondition(ratioDown,valExpect,valFeePercent=0.000):
	return getMinRate(ratioDown,valExpect) > valFeePercent*(2+calMaxRate(ratioDown,valExpect))

def calBuyAmount(fundRemain,valExpect):
	return fundRemain*(valExpect**2)

def getRateToSell(numStep):
	#step = 5 => 30%
	#step = 4 => 30%
	#step = 3 => 20%
	#step = 2 => 10%
	#step = 1 => 10%
	#-1/6*(x^3-6x^2+5x-6)
	
	return -1*((numStep**3)-6*(numStep**2)+5*numStep)/60+0.1
	
def calSellAmount(amountBitCoin,numStep=0):
	return amountBitCoin*getRateToSell(numStep)

def calSellPrice(pricePeak,priceBuy,numStep=0,unitCurrency=100.0):
	priceSellReal = (numStep+1)*0.2*calDigByPrices(pricePeak,priceBuy)+priceBuy
	priceSellUnit = math.ceil(priceSellReal/unitCurrency)
	priceSellQuantized = priceSellUnit*unitCurrency
	
	return priceSellQuantized

print getExpectationRatio(1000,5000,0.05)
print getExpectationRatio(1000,5000,0.5)
print getExpectationRatio(1000,5000,1)
print getExpectationRatio(1000,5000,5)
print getExpectationRatio(4000,5000,0.05)
print getExpectationRatio(4000,5000,0.5)
print getExpectationRatio(4000,5000,1)
print getExpectationRatio(4000,5000,5)
print getExpectationRatio(10000,5000,0.05)
print getExpectationRatio(10000,5000,0.5)
print getExpectationRatio(10000,5000,1)
print getExpectationRatio(10000,5000,5)