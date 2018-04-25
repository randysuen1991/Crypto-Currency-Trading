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
    
def visualize():
    import  matplotlib.pyplot as plt
    import os
    import numpy as np
    from statsmodels.tsa.stattools import adfuller
    from strategies import PairTrading
    
    
    
    
    
    data = list()
    for file in os.listdir('C:\\Users\\ASUS\\Dropbox\\pycode\\mine\\Crypto-Currency-Trading\\data'):
        print(file)
        file = 'C:\\Users\\ASUS\\Dropbox\\pycode\\mine\\Crypto-Currency-Trading\\data\\' + file
        data.append(np.load(file,'r'))
    
    standardized_data = list()
    #standardize the data
    for data_single in data :
        m = np.mean(data_single)
        s = np.std(data_single)
        new_list = [(d-m)/s for d in data_single]
        standardized_data.append(new_list)
#    print(np.std(standardized_data[0]))
        
    c1 = 1
    c2 = 6
    lm, difference = PairTrading.LogistLinearRegression(data[c1],data[c2])
    
    
#    difference = [a-b for a, b in zip(standardized_data[c1],standardized_data[c2])]
    
    plt.plot(difference,'-b',label='residual')
    plt.legend(loc=0)
    result = adfuller(difference)
    print(result[0],result[1])

#    plt.xlabel('time')
#    plt.ylabel('price')
    
if __name__ == '__main__':
    visualize()
#    example1()