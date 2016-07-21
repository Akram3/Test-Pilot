import pandas as pd
import oandapy
import os

class Hawkes(oandapy.Streamer,object):
    def __init__(self,*args,**kwargs):
        oandapy.Streamer.__init__(self,account_number,access_token)
        self.ticks = 0

    def on_success(self, data):
        self.ticks += 1
        print(data)
        if self.ticks == 10:
            self.disconnect()
    def on_error(self, data):
        self.disconnect()

    def invested():
        i = alpha.get_trades(account_id=account_number)['trades']
    return i

    def buy(units):
        buy = alpha.create_order(account_id=account_number,
                                instrument='EUR_USD',
                                units= units,
                                side='buy',
                                type='market')
        return sell
    def sell(units):
        sell = alpha.create_order(account_id=account_number,
                                instrument='EUR_USD',
                                units= units,
                                side='sell',
                                type='market')
        return sell
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

if __name__ == '__main__':
    account_number = os.getenv("practice_number")
    access_token = os.getenv("practice_access_token")
    stream = Hawkes(environment="practice",access_token=access_token)
    stream.start(accountId=account_number, instruments="EUR_USD")
