import numpy as np
from Requests import Request
from sklearn import linear_model
import websockets as WS
import asyncio


class PairTrading():
    
    # This class method returns the residuals of the logistLinearRegression
    @classmethod
    def LogistLinearRegression(cls,price_x,price_y):
        lm = linear_model.LinearRegression()
        logy = np.log(price_y)
        logx = np.log(price_x)
        lm.fit(logx,logy)
        res_train = logy - lm.predict(logx)
        return lm, res_train
    
    
    # The amount should be the number we are gonna trade, lm is the linear model, and the account should 
    # be the account of the trader.
    @classmethod
    @asyncio.coroutine
    def PairTrade(cls, crypto_x, crypto_y, price_x, price_y, amount, lm, sigma, account, **kwargs):
        num_sigma = kwargs.get('num_sigma',2)
        if np.log(price_y) - lm.predict(np.log(price_x)) > num_sigma * sigma :
            yield from cls.Trade(amount,crypto_x,crypto_y,account,cond='over')
        elif np.log(price_y) - lm.predict(np.log(price_x)) < num_sigma * sigma :
            yield from cls.Trade(amount,crypto_x,crypto_y,account,cond='under')
            
            
    @classmethod
    @asyncio.coroutine
    def Trade(cls, amount, crypto_x, crypto_y, account,cond):
        if cond == 'over' : 
            crypto = lambda x, y: x if x > y else y
            yield from WS.send(Request.Place_Order(crypto=crypto(crypto_x,crypto_y,amount)))
            if account[crypto_y] > account[crypto_x] :
                yield from WS.send(Request.Place_Order(crpyto_y,amount,price,type='sell'))
            else :
                yield from WS.send(Request.Place_Order(crypto_x,amount,price,type='buy'))
                
        elif cond == 'under' :
            
            pass