# Crypto-Currency-Trading
Till now, this is a repository which stores code to download real-time crypto currency price. It uses the python asychronous computing technique. <br>
I would continue updating the contents as soon as possible.

## The trend of the cryptocurrency in a period of time.
The first two figures are the prices of BTC and XRP in a period of time on 4/24/2018. <br>

![](https://github.com/randysuen1991/Crypto-Currency-Trading/blob/master/figures/btc.png)
![](https://github.com/randysuen1991/Crypto-Currency-Trading/blob/master/figures/xrp.png)<br>

The following figure is log(price_btc) - ( alpha + beta * log(price_xrp) ), where alpha and beta are obtained by least square.<br>
The p-value of ADFuller test is 0.0005 < 0.05. So we might be able to assume the residual is stationary process.
![](https://github.com/randysuen1991/Crypto-Currency-Trading/blob/master/figures/res_btc_xrp.png)

Therefore, **PairTrading** might be a good strategy.