import TradeBase

def example1():
    trader = TradeBase.Trader()
    trader.Connect()
    trader.Collect_Data_Ticker(delay_time=10,num_data=300)
    trader.Start()
    
def example2():
    trader = TradeBase.Trader()
    trader.Connect()
    trader.Subscribe_Order_Book(crypto='XRP',money='USD',depth=10,subscribe=True,delay_time=1)
    trader.Start()
    
def visualize():
    import  matplotlib.pyplot as plt
    import os
    import sys
    import numpy as np
    sys.path.append('C:\\Users\\ASUS\\Dropbox\\pycode\\mine\\Crypto-Currency-Trading\\data')
    name = ['bch','btc','btg','dash','eth','xlm','xrp','zec']
    for file, name in zip(os.listdir('C:\\Users\\ASUS\\Dropbox\\pycode\\mine\\Crypto-Currency-Trading\\data'),name):
        print(file,name)
        np.load(file,name)
if __name__ == '__main__':
    visualize()