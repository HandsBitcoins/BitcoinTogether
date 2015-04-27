class InfoBuy(object):
    def __init__(self, isBuy, priceCrest, priceTrough, priceNow):
        self.isBuy = isBuy
        self.priceCrest = priceCrest
        self.priceTrough = priceTrough
        self.priceNow = priceNow

class InfoSell(object):
    def __init__(self, priceBid, amountBid):
        self.priceBid = priceBid
        self.amountBid = amountBid
  