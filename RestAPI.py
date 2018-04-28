import requests as rq
import time
import numpy as np

url_xrp = "https://cex.io/api/ticker/XRP/USD"
url_btc = "https://cex.io/api/ticker/BTC/USD"
ask_xrp = []
bid_xrp = []
ask_btc = []
bid_btc = []
count = 0
while (True and count<5):
    result_xrp = rq.get(url=url_xrp)
    result_json_xrp = result_xrp.json()
    new_bid_xrp = result_json_xrp["bid"]
    new_ask_xrp = result_json_xrp["ask"]
    bid_xrp.append(new_bid_xrp)
    ask_xrp.append(new_ask_xrp)
    
    result_btc = rq.get(url=url_btc)
    result_json_btc = result_btc.json()
    new_bid_btc = result_json_btc["bid"]
    new_ask_btc = result_json_btc["ask"]
    bid_btc.append(new_bid_btc)
    ask_btc.append(new_ask_btc)
    
    count = count + 1
    print("Fetching ",count,"times....")
    time.sleep(1)
    
np.save("ask_history_xrp",ask_xrp)
np.save("bid_history_xrp",bid_xrp)
np.save("ask_history_btc",ask_btc)
np.save("bid_histort_btc",bid_btc)



