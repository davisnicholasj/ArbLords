import gdax
from poloniex import Poloniex
import pandas as pd

#### Polo Data
polo = Poloniex()
orders = polo.returnOrderBook()['BTC_ETH']

poloAsks = pd.DataFrame(orders['asks'])
poloAsks.columns = ['price','volume']
poloAsks = poloAsks.astype(float)

poloBids = pd.DataFrame(orders['bids'])
poloBids.columns = ['price','volume']
poloBids = poloBids.astype(float)


#### GDAX Data
public_client = gdax.PublicClient()
wsClient = gdax.WebsocketClient(url="wss://ws-feed.gdax.com", products="ETH-BTC")

gdaxEthBtcOrderBook = public_client.get_product_order_book('ETH-BTC', level=2)

bids = dict.get(gdaxEthBtcOrderBook,'bids')
asks = dict.get(gdaxEthBtcOrderBook,'asks')
wsClient.close()


gdaxBids = pd.DataFrame(bids)
gdaxBids.columns = ["price","volume","orders"]
gdaxBids = gdaxBids.astype(float)

gdaxAsks = pd.DataFrame(asks)
gdaxAsks.columns = ["price","volume","orders"]
gdaxAsks = gdaxAsks.astype(float)


#### ETH balances currently hardcoded as 20 for testing
#### In the future, we'll need to add logic to check all of our exchanges to decide which pairings we'll be buying/selling 
ethGdax = 20
tempGdaxPrice = gdaxAsks[gdaxAsks['volume'] > ethGdax].iloc[0,0]
ethPolo = 20
tempPoloPrice = poloBids[poloBids['volume'] > ethPolo].iloc[0,0]


################################
################################


#### Static values for testing

balGdax = 20000
balPolo = 20000
balTotal = balGdax + balPolo

ethGdax = 20.0
ethPolo = 20.0
ethTotal = ethGdax + ethPolo

priceGdax = 700
pricePolo = 688

fee = 0.0025

#### Start calculations


#### Check to see if we have enough USD balance in our Polo account to be able to sell our full stack of ETH on GDAX
usdLimitingFlag = (ethGdax * priceGdax) < balPolo

if usdLimitingFlag == True:
    print('We have plenty of USD to throw around in our Polo balance - normal arb')
    
    #### Sell all of our ETH on GDAX, acquire USD
    balChangeGdax = ethGdax * priceGdax
    ethChangeGdax = 0 - ethGdax
    
    #### When we buy ETH on Polo, they take a fee out of each purchase (comes out of our final ETH balance)
    balChangePolo = -1.0 * balChangeGdax
    ethChangePolo = (balChangeGdax / (1.0 + fee)) / pricePolo
    
    #### Calculate our theoretical final USD balances on each exchange after making the trade 
    balGdaxFinal = balGdax + balChangeGdax
    balPoloFinal = balPolo + balChangePolo

    ### Calculate our theoretical final ETH balances on each exchange after making the trade 
    ethPoloFinal = ethPolo + ethChangePolo
    ethGdaxFinal = ethGdax + ethChangeGdax

else: 
    print('We are limited by our current Polo USD balance - so we will limit how much ETH we sell on GDAX so that we dont lose ETH in the process. We want to come away with more ETH rather than coming away with more USD')
    
    #### Limited by our Polo balance, so we'll only sell however many ETH on GDAX as we have in our USD balance on Polo
    limitingETH = balPolo / priceGdax
    
    #### Limit how much ETH we sell on GDAX to make sure we don't lose ETH in favor of profiting in more USD
    ethChangeGdax = -1.0 * limitingETH
    balChangeGdax = limitingETH * priceGdax

    #### When we sell ETH on Polo, they take a fee out of each purchase (comes out of our final ETH balance)
    balChangePolo = -1.0 * balChangeGdax
    ethChangePolo = (balPolo / (1.0 + fee)) / pricePolo

    #### Calculate our theoretical final USD balances on each exchange after making the trade 
    balGdaxFinal = balGdax + balChangeGdax
    balPoloFinal = balPolo + balChangePolo

    ### Calculate our theoretical final ETH balances on each exchange after making the trade 
    ethPoloFinal = ethPolo + ethChangePolo
    ethGdaxFinal = ethGdax + ethChangeGdax

#### Calculate how much we're losing in fees
exchangeFee = balPolo - (balPolo / (1 + fee))

#### Calculate our final totals in both USD and ETH 
usdTotalFinal = balGdaxFinal + balPoloFinal
ethTotalFinal = ethGdaxFinal + ethPoloFinal

#### ETH total should have increased and USD should stay flat (or slightly decreased)
usdGains = usdTotalFinal - balTotal
ethGains = ethTotalFinal - ethTotal

#### Purely for illustration - calculating our estimated ETH gains in common USD
ethToDollarGains = ethGains * max(priceGdax, pricePolo)

totalArbValue = ethToDollarGains + usdGains 

print("Total dollar difference: " + str(usdGains))
print("Total ETH difference: " + str(ethGains))


print("Exchange fee: $" + str(exchangeFee))
print("Total arb value: $" + str(totalArbValue))




##### Will need to rebalance the USD amounts between the two wallets after this. Costs .002 ETH to send from Bittrex
#### Costs .002 ETH to withdraw from Bittrex
#### Costs .005 ETH to withdraw from Polo
#### Costs .0001 BTC to withdraw from Polo
#### No withdrawal costs from GDAX


print('balTotal ' + str(balTotal))
print('balGdax ' + str(balGdax))
print('balPolo ' + str(balPolo))
print('ethTotal ' + str(ethTotal))

print('balGdaxFinal ' + str(balGdaxFinal))
print('balPoloFinal ' + str(balPoloFinal))
print('balTotalFinal ' + str(usdTotalFinal))

print('ethPoloFinal ' + str(ethPoloFinal))
print('ethGdaxFinal ' + str(ethGdaxFinal))
print('ethTotalFinal ' + str(ethTotalFinal))


#### Calculate how much ETH and BTC/USD will need to be rebalanced 

def reBalEth():
    ethreBal = (ethTotalFinal / 2)
    if ethPoloFinal > ethreBal:
        ethToSend = ethPoloFinal - ethreBal
        print(ethToSend)
    elif ethGdaxFinal > ethreBal:
        ethToSend = ethGdaxFinal - ethreBal
        print(ethToSend)
    else: 
        print("all good")

def reBalCoin():
    coinReBal = (usdTotalFinal / 2)
    if balPoloFinal > coinReBal:
        balToSend = balPoloFinal - coinReBal
        print(balToSend)
    elif balGdaxFinal > coinReBal:
        balToSend = balGdaxFinal - coinReBal
        print(balToSend)
    else: 
        print("all good")        
        
        
reBalEth()
reBalCoin()
