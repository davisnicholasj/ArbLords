#while True:

# ccxt is the source import to call many exchanges.  https://github.com/ccxt/ccxt is the source code & documentation
# import ccxt

#gdax Python API docs: https://github.com/danpaquin/gdax-python
import gdax #pip install gdax
import bitfinex
from bittrex import Bittrex, API_V2_0, API_V1_1  #pip install pip install python-bittrex
from geminipy import Geminipy #pip install geminipy
from poloniex import Poloniex #pip3 install https://github.com/s4w3d0ff/python-poloniex/archive/v0.4.6.zip     https://github.com/s4w3d0ff/python-poloniex/blob/master/poloniex/__init__.py
#from binance.client import Binance #pip install python-binance


booty 
#"
# Get mid-market price of a given Crypto
# Get top 50 prices/volume from both sides of the order book
# Get balance of a given crypto
# Get USD balance
# Execute trade against a given pairing
# Withdraw an asset to a specific address
# "


import csv
#variables to store the API for each exchange
GDAX = gdax.PublicClient()
my_gdax = gdax.AuthenticatedClient('afb5c86acff788d5f92f11464778b3fc','bhG2QcCgdYhxUrdYtaGC2RI6rgZ/3nnD4iIk44fkm1ddLflIA5MESMfiAVF7FM3LAe0NFJ8LJ3O3kM+1eCUXgA==','phrigmphragm69')
polo = Poloniex('VVON608N-R94HR9YS-IBLCJJPZ-SZ6BNQO9','f122cbc7d88c083b9c60483d6d7be5637b8ba808812bafa678fb87d6a04a5ae5d54b3b7dc04422366e41bbfc5e491f073a2b328c8a453918c7537c48ef465311')
Bitfinex = bitfinex.Client()
gem = Geminipy(api_key='',secret_key='',live=True)
my_bittrex = Bittrex('2a1e0d61c5804c1fa2f36f7bd5abe293', '98558cc7b793450d8290630010550994', api_version=API_V2_0)

poloBalance = polo.returnBalances()


print(polo.returnTicker()['BTC_ETH'])

# print(Bitfinex.ticker('ETHBTC'))

#"
# AUTHENTICATION - DO NOT FUCK WITH THIS
# "




print("polo call")
print(float(dict.get(polo.returnTicker()['BTC_ETH'],'last')))

# print("bittrex call")
# print(my_bittrex.get_balance('OMG'))

# gemBook = gem.pubticker('ethbtc')
# print(gemBook.json())
    



#"
# Instantiation of private variables to be used across the entire script
# "
initialInvestmentETH = 10.0 #to be updated with the amount initially deposited
initialInvestmentBTC = 10.0 # should be updated with the amount initially deposited
poloETH = float(dict.get(polo.returnBalances())) # to be replaced with amount of ETH from Bithumb API
poloBTC = 5.0  # to be replaced with amount of BTC from BitHumb API
gdaxBTC = float(dict.get(my_gdax.get_account('d33de849-a1dc-4b12-be69-64b17098b45d'),'available')) # API makes a call to GDAX to pull BTC balances and convert them to a float
gdaxETH = float(dict.get(my_gdax.get_account('38857d4e-3aaa-4d13-8306-ed0667c7336c'),'available')) # API makes a call to GDAX to pull ETH balances and convert them to a float
totalETH = poloETH + gdaxETH
totalBTC = poloBTC + gdaxBTC
balanceGdax = 0.0
balancePolo = 0.0

print("gdax call")
print(gdaxETH)

gdaxEthBtcOrderBook = GDAX.get_product_order_book('ETH-BTC', level=1)



bids = dict.get(gdaxEthBtcOrderBook,'bids')
asks = dict.get(gdaxEthBtcOrderBook,'asks')

# with open('log.csv','w',newline='') as csvfile:
#     logWriter = csv.writer(csvfile, delimiter = ',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
#     logWriter.writerow(bids)
#     logWriter.writerow(asks)

# priceList = []
# for bid in bids:
#     priceList.append(float(bid[0]))
# print(priceList)
# bidList = [item for sublist in bids for item in sublist]
# askList = [item for sublist in asks for item in sublist]
# print(bidList[1])