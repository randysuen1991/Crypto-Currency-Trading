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
    import numpy as np
    name = ['bch','btc','btg','dash','eth','xlm','xrp','zec']
    for file, name in zip(os.listdir('C:\\Users\\ASUS\\Dropbox\\pycode\\mine\\Crypto-Currency-Trading\\data'),name):
        print(file,name)
        file = 'C:\\Users\\ASUS\\Dropbox\\pycode\\mine\\Crypto-Currency-Trading\\data\\' + file
        np.load(file,'r')
    plt.plot()
if __name__ == '__main__':
    visualize()