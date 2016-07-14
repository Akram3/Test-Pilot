
# coding: utf-8

# In[3]:

import pandas as pd 
import oandapy 
import os 
from datetime import datetime, timedelta
from v20.authorization import EntitySpec

import time

account_number =2572666
access_token = "5bc15f7110f8c9017e81e784a41b73e8-816783705fe8edb29bd0829451bb5eb6"

trade_expire = datetime.now() + timedelta(days=1)
trade_expire = trade_expire.isoformat('T') + 'Z'

alpha = oandapy.API(environment="practice" , access_token=access_token)

def invested():
    i = alpha.get_trades(account_id=account_number)['trades']
    return i

def macd(df,q,p,m,n):
    k = df.ewm(span=m).mean() - df.ewm(span=n).mean()
    m = k.ewm(span=q).mean()
    s = k.ewm(span=p).mean()
    b = (m-s).ewm(span=q).mean()
    return m,s,b

def BB(dataFrame,period,n):
    upper = dataFrame.ewm(span=period).mean()+dataFrame.ewm(span=period).std()*n
    mid =  dataFrame.ewm(span=period).mean()
    lower = dataFrame.ewm(span=period).mean()-dataFrame.ewm(span=period).std()*n
    return upper,mid,lower

def price_change():    # same as pdiff
    bool_ = np.diff(mid) > 0
    return bool_
        
#from pykalman import KalmanFilter
#kf = KalmanFilter(initial_state_mean=0,n_dim_obs=2)
#measurements = zip(mid_prices,range(len(mid_prices)))

# Run simulated trades on demo account

while True:
    try:
        eur_usd = alpha.get_history(instrument="EUR_USD",
                                      granularity='S5',
                                      count = 50,)
        eur_usd_M5 = alpha.get_history(instrument="EUR_USD",
                                      granularity='M1',
                                      count = 50,)
        hist_tick_data = pd.DataFrame(eur_usd['candles'],
                              ).drop('time',1)
    
        hist_tick_data_M5 = pd.DataFrame(eur_usd_M5['candles'],
                              ).drop('time',1)
        mid_prices = (hist_tick_data['closeAsk']+hist_tick_data['closeBid'])/2.
        mid_prices_M5 = (hist_tick_data_M5['closeAsk']+hist_tick_data_M5['closeBid'])/2.
    
        ask = alpha.get_prices(instruments="EUR_USD")['prices'][0]['ask']
        bid = alpha.get_prices(instruments="EUR_USD")['prices'][0]['bid']
        spread = (abs(ask-bid))
        mid_price = (ask+bid)/2.
        
        
        target_buy = BB(mid_prices,26,2.4)[0][49]
        target_sell = BB(mid_prices,26,2.4)[2][49]
        stop_loss_buy = BB(bid,26,2)[0][49] # Stop loss at 3 std of historical revese order flow 
        stop_loss_sell = BB(ask,26,2)[2][49] # Stop loss at 3 std of historical revese order flow
        
        SIGNAL_1 = macd(mid_prices,3,9,12,26)
        SIGNAL_2 = macd(mid_prices_M5,3,9,12,26)

        if hist_tick_data['volume'][49]>1 and (SIGNAL_1[2][49])>0 and (SIGNAL_2[2][49]>0)  and invested() == []:
            alpha.create_order(account_id=account_number,
                        instrument='EUR_USD',
                        units= 100,
                        side='buy',
                        type='market',
                        takeProfit=round(target_buy,3),
                        stopLoss=round(stop_loss_buy,3))
    
        elif hist_tick_data['volume'][49]>1 and (SIGNAL_1[2][49])<0 and (SIGNAL_2[2][49]<0)  and invested() == []:
            alpha.create_order(account_id=account_number,
                        instrument='EUR_USD',
                        units= 100,
                        side='sell',
                        takeProfit=round(target_sell,3),
                        type='market',
                        stopLoss=round(stop_loss_sell,3))

        elif invested() != [] and SIGNAL_2[1][49]==0:
            alpha.close_position(account_id=account_number,instrument="XAU_USD")
            if price_change()==True:
                alpha.create_order(account_id=account_number,
                        instrument='EUR_USD',
                        units= 100,
                        side='buy',
                        type='market',
                        takeProfit=round(target_buy,3),
                        stopLoss=round(stop_loss_buy,3))
                
            else:
                alpha.create_order(account_id=account_number,
                        instrument='EUR_USD',
                        units= 100,
                        side='sell',
                        takeProfit=round(target_sell,3),
                        type='market',
                        stopLoss=round(stop_loss_sell,3))
    except Exception as e:
            print('hmm... :'+str(e))

