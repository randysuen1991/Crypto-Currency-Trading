import TradeBase

def example1():
    trader = TradeBase.Trader()
    trader.Connect()
    trader.Collect_Data_Ticker(delay_time=10,num_data=500)
    trader.Start()
    
def example2():
    trader = TradeBase.Trader()
    trader.Connect()
    trader.Subscribe_Order_Book(crypto='XRP',money='USD',depth=10,subscribe=True,delay_time=1)
    trader.Start()


def example3():
    trader = TradeBase.Trader()
    trader.Connect()
    trader.PairTrade(crypto_x='BTC',crypto_y='XRP',money='USD',delay_time=10,num_data=300,num_sigma=100,amount=40)
    trader.Start()

def visualize():
    import  matplotlib.pyplot as plt
#    import sys
    import numpy as np
    from statsmodels.tsa.stattools import adfuller
    from strategies import PairTrading
    
    
#    sys.path.append('C:\\Users\\ASUS\\Dropbox\\pycode\\mine\\Crypto-Currency-Trading\\data\\')
    
    data = np.load('data2.npy')
    lm, res = PairTrading.LogistLinearRegression(data['BTC'],data['XRP'])
    plt.plot(res,'-b',label='residual')
    result = adfuller(res)
    plt.legend(loc=0)
    print(result[0],result[1])

    plt.xlabel('time')
    plt.ylabel('price')
    
if __name__ == '__main__':
    visualize()
#    example3()