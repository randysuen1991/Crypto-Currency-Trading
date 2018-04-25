import hmac
import hashlib
import datetime
import json
import websockets as WS
import asyncio
import pickle
import numpy as np
from Requests import Request
from strategies import PairTrading
    
class Trader(object):

    def __init__(self):
        self.key = 'ZX1jQggifgNgEQoQfllsV1VtrV0'
        self.secret = 'nUBLBFHA6A0TgkgMfDsLuIctkBI'
        self.loop = self._Set_Event()
        self.ws = None
        self.orders = dict()
        self.complete = False
        self.iteration = 0
        self.buffer = dict()
        # We should add a more method to unpickle the dictionary (i.e load data into a trader.training_data) from the directory.
        self.training_data = {
                                'BTC':{'high':[],'low':[],'last':[]},
                                'ETH':{'high':[],'low':[],'last':[]},
                                'BCH':{'high':[],'low':[],'last':[]},
                                'BTG':{'high':[],'low':[],'last':[]},
                                'DASH':{'high':[],'low':[],'last':[]},
                                'XRP':{'high':[],'low':[],'last':[]},
                                'XLM':{'high':[],'low':[],'last':[]},
                                'ZEC':{'high':[],'low':[],'last':[]},
                                }
        # This account is a dictionary with key equal to the symbol of the cryptocurrency and the value be the number of it.
        self.account = dict()
        
    def _Create_signature(self,key, secret):  # (string key, string secret) 
        timestamp = int(datetime.datetime.now().timestamp())  # UNIX timestamp in seconds
        string = "{}{}".format(timestamp, key)
        return timestamp, hmac.new(secret.encode(), string.encode(), hashlib.sha256).hexdigest()

    def _Auth_request(self):
        timestamp, signature = self._Create_signature(self.key, self.secret)
        return json.dumps({
                            'e': 'auth',
                            'auth': {
                                    'key': self.key, 'signature': signature, 'timestamp': timestamp,}, 'oid': 'auth', 
                                    })
    
    def Start(self):
        self.loop.run_forever()
#        try:
#            self.loop.run_forever()
#        except KeyError:
#            print('ttt')
#        except WS.exceptions.ConnectionClosed:
#            print('connectionclose')
#            self.loop.close()
            
    def _Set_Event(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        return asyncio.get_event_loop()
    def Reset_Event(self):
        print('Reset')
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.loop = asyncio.get_event_loop()
        
    def Connect(self):
        asyncio.ensure_future(self._Connect())
        
        
    @asyncio.coroutine
    def _Connect(self):
        
        self.ws = yield from WS.connect('wss://ws.cex.io/ws/')
        yield from self.ws.send(self._Auth_request())
        yield from self.ws.recv()
        result = yield from self.ws.recv()
        print(result)
        
    
    @asyncio.coroutine
    def _Send_Ticker_Recv_Result(self,crypto):
        yield from self.ws.send(Request.Ticker(crypto,'USD'))
        result_json = yield from self.ws.recv()
        print(result_json)
        try:
            result = json.loads(result_json)['data']
        # KeyError would happen when the 'ping pong' problem happens. So, just save the current data.
        except KeyError:
            print('Ping Pong problem occurs.')
            self.loop.stop()

        self.training_data[crypto]['high'].append(float(result['high']))
        self.training_data[crypto]['low'].append(float(result['low']))
        self.training_data[crypto]['last'].append(float(result['last']))
        
            
            
    @asyncio.coroutine
    def _Sleep(self,delay_time):
        if delay_time >= 15:
            asyncio.ensure_future(self._Get_Ping(delay_time))

        # we accept for each 'ping', it might delay 0.25 sec.
        yield from asyncio.sleep(delay_time+int(delay_time/15)*0.25)
    # The following function isn't done since we might get many 'ping'.
    @asyncio.coroutine
    def _Get_Ping(self,delay_time):
        loop_times = int(delay_time/15)
        for time in range(loop_times):
            ping = yield from self.ws.recv()
            print(ping)
            yield from self.ws.send(Request.Pong())
            print(Request.Pong())
            
    def Collect_Data_Ticker(self,delay_time,num_data):
        asyncio.ensure_future(self._Collect_Data_Ticker(delay_time,num_data))
        
    @asyncio.coroutine
    def _Collect_Data_Ticker(self,delay_time,num_data):
        # Let the connecting coroutine connect first. So sleep awhile.  
        yield from asyncio.sleep(3)
        count = 0
        try:
            while True:
                
                yield from asyncio.wait([self._Send_Ticker_Recv_Result('BTC'),
                                         self._Send_Ticker_Recv_Result('ETH'),
                                         self._Send_Ticker_Recv_Result('BCH'),
                                         self._Send_Ticker_Recv_Result('BTG'),
                                         self._Send_Ticker_Recv_Result('DASH'),
                                         self._Send_Ticker_Recv_Result('XRP'),
                                         self._Send_Ticker_Recv_Result('XLM'),
                                         self._Send_Ticker_Recv_Result('ZEC')])
    
                
                
                if count == num_data :
                    break
                else : 
                    yield from self._Sleep(delay_time)
                count += 1
        except AttributeError:
            raise NotImplementedError('You should Connect to the server first.')
        
        
        finally:
            #picke the training data to the directory
            pickle_out = open('training_data_new','wb')
            pickle.dump(self.training_data,pickle_out)
            pickle_out.close()
            self.complete = True
            self.loop.stop()
    
    def Subscribe_Order_Book(self,crypto,money='USD',subscribe=False,depth=-1,delay_time=5):
        asyncio.ensure_future(self._Subscribe_Order_Book(crypto,money,subscribe,depth,delay_time))
        
    @asyncio.coroutine
    def _Subscribe_Order_Book(self,crypto,money,subscribe,depth,delay_time):
        # Let the connecting coroutine connect first. So sleep awhile.  
        
        yield from asyncio.sleep(3)
        yield from self.ws.send(Request.Order_Book(crypto=crypto,money=money,subscribe=subscribe,depth=depth))
        for count in range(100):
            print(count)
            result_json = yield from self.ws.recv()
            result = json.loads(result_json)
            print(result)
            yield from self.ws.send(Request.Pong())
            yield from asyncio.sleep(delay_time)
            
        self.loop.stop()
    
    
    
    @asyncio.coroutine
    def _Send_Ticker_Append_Result(self,crypto):
        yield from self.ws.send(Request.Ticker(crypto,'USD'))
        result_json = yield from self.ws.recv()
        try:
            result = json.loads(result_json)['data']
        # KeyError would happen when the 'ping pong' problem happens. So, just save the current data.
        except KeyError:
            print('Ping Pong problem occurs.')
            self.loop.stop()
            
        
        
        # I use last 250 data as the traing for the new realization.
        if len(self.buffer[crypto]) == 251 :
            self.buffer[crypto].pop()
            
        self.buffer[crypto].append(float(result['last']))
        
        
        
    def PairTrade(self,crypto_x,crypto_y,delay_time,num_data,num_sigma,amount,money='USD'):
        asyncio.ensure_future(self._PairTrade(crypto_x,crypto_y,money,delay_time,num_data,num_sigma,amount))
    
    @asyncio.coroutine
    def _PairTrade(self,crypto_x,crypto_y,money,delay_time,num_data,num_sigma,amount):
        self.buffer[crypto_x] = list()
        self.buffer[crypto_y] = list()
        
        yield from asyncio.sleep(3)
        
        
        
        # Get the information of my account
        yield from self.ws.send(Request.Get_Balance())
        result_json = yield from self.ws.recv()
        result = json.loads(result_json)
        self.account = result['data']['balance']
        print(self.account)
        count = 0
        try :
            while True:
                yield from asyncio.wait([
                                        self._Send_Ticker_Append_Result(crypto_x),
                                        self._Send_Ticker_Append_Result(crypto_y)
                                        ])
    
                print(self.buffer)
                if len(self.buffer[crypto_x]) > 2 :
                    lm, res = PairTrading.LogistLinearRegression(self.buffer[crypto_x][0:250],self.buffer[crypto_y][0:250])
                    sigma = np.std(res)
                    if sigma > 0 :
                        yield from PairTrading.PairTrade(crypto_x,crypto_y,self.buffer[crypto_x][-1],self.buffer[crypto_y][-1],lm=lm,amount=amount,sigma=sigma,account=self.account,num_sigma=num_sigma)
                    
                count += 1
                if count ==  num_data :
                    break
                else :
                    yield from self._Sleep(delay_time)
                    
                    
        except AttributeError:
            raise NotImplementedError('You should Connect to the server first.')
        
        finally :
            pass
    