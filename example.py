import TradeBase

def example1():
    trader = TradeBase.Trader()
    trader.Connect()
    trader.Collect_Data_Ticker(delay_time=5,num_data=100)
    trader.Start()
    
def example2():
    trader = TradeBase.Trader()
    trader.Connect()
    trader.Subscribe_Order_Book(crypto='XRP',money='USD',depth=10,subscribe=True,delay_time=1)
    trader.Start()
    
    
if __name__ == '__main__':
    example1()